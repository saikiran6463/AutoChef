from aws_cdk import (
    Stack,
    Duration,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_logs as logs,
    aws_servicediscovery as servicediscovery,
    aws_iam as iam,
    RemovalPolicy
)
from constructs import Construct

class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ========================================
        # Container Registry (ECR) Setup
        # ========================================
        
        # ECR Repository for Java Spring Boot Service
        self.java_service_repo = ecr.Repository(
            self, "AutoChefJavaServiceRepo",
            repository_name="autochef-java-service",
            image_scan_on_push=True,  # Security scanning
            removal_policy=RemovalPolicy.DESTROY  # For learning/demo - remove in production
        )
        
        # ECR Repository for Python FastAPI Service
        self.python_service_repo = ecr.Repository(
            self, "AutoChefPythonServiceRepo", 
            repository_name="autochef-python-service",
            image_scan_on_push=True,  # Security scanning
            removal_policy=RemovalPolicy.DESTROY  # For learning/demo - remove in production
        )
        
        # ========================================
        # Networking Infrastructure (VPC)
        # ========================================
        
        # Create VPC with public and private subnets across 2 AZs
        self.vpc = ec2.Vpc(
            self, "AutoChefVPC",
            vpc_name="autochef-vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,  # Use 2 Availability Zones for high availability
            subnet_configuration=[
                # Public subnets for Load Balancer
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24  # 10.0.1.0/24, 10.0.2.0/24
                ),
                # Private subnets for ECS services 
                ec2.SubnetConfiguration(
                    name="PrivateSubnet", 
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24  # 10.0.11.0/24, 10.0.12.0/24
                )
            ],
            nat_gateways=1  # 1 NAT Gateway for cost optimization (use 2 for production)
        )
        
        # ========================================
        # Security Groups
        # ========================================
        
        # Security Group for Application Load Balancer
        self.alb_security_group = ec2.SecurityGroup(
            self, "ALBSecurityGroup",
            vpc=self.vpc,
            description="Security group for AutoChef Application Load Balancer",
            allow_all_outbound=True
        )
        
        # Allow HTTP traffic from internet to ALB
        self.alb_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP traffic from internet"
        )
        
        # Allow HTTPS traffic from internet to ALB (for future SSL)
        self.alb_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(), 
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS traffic from internet"
        )
        
        # Security Group for ECS Services
        self.ecs_security_group = ec2.SecurityGroup(
            self, "ECSSecurityGroup",
            vpc=self.vpc,
            description="Security group for AutoChef ECS Services",
            allow_all_outbound=True  # Allow outbound for AWS Bedrock calls
        )
        
        # Allow traffic from ALB to ECS services
        self.ecs_security_group.add_ingress_rule(
            peer=self.alb_security_group,
            connection=ec2.Port.tcp(8080),  # Java service port
            description="Allow traffic from ALB to Java service"
        )
        
        self.ecs_security_group.add_ingress_rule(
            peer=self.alb_security_group,
            connection=ec2.Port.tcp(8000),  # Python service port
            description="Allow traffic from ALB to Python service"
        )
        
        # Allow ECS services to communicate with each other
        self.ecs_security_group.add_ingress_rule(
            peer=self.ecs_security_group,
            connection=ec2.Port.all_traffic(),
            description="Allow ECS services to communicate with each other"
        )
        
        # ========================================
        # Application Load Balancer (ALB)
        # ========================================
        
        # Create Application Load Balancer in public subnets
        self.load_balancer = elbv2.ApplicationLoadBalancer(
            self, "AutoChefALB",
            vpc=self.vpc,
            internet_facing=True,  # Internet-facing ALB
            security_group=self.alb_security_group,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC  # Deploy in public subnets
            )
        )
        
        # Create Target Group for Java Service (API Gateway)
        self.java_target_group = elbv2.ApplicationTargetGroup(
            self, "JavaServiceTargetGroup",
            vpc=self.vpc,
            port=8080,
            protocol=elbv2.ApplicationProtocol.HTTP,
            target_type=elbv2.TargetType.IP,  # Required for Fargate
            health_check=elbv2.HealthCheck(
                path="/actuator/health",  # Spring Boot Actuator health endpoint
                healthy_http_codes="200",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(10),
                healthy_threshold_count=2,
                unhealthy_threshold_count=5
            )
        )
        
        # Create Target Group for Python Service (LLM Service)
        self.python_target_group = elbv2.ApplicationTargetGroup(
            self, "PythonServiceTargetGroup", 
            vpc=self.vpc,
            port=8000,
            protocol=elbv2.ApplicationProtocol.HTTP,
            target_type=elbv2.TargetType.IP,  # Required for Fargate
            health_check=elbv2.HealthCheck(
                path="/health",  # FastAPI health endpoint
                healthy_http_codes="200",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(10),
                healthy_threshold_count=2,
                unhealthy_threshold_count=5
            )
        )
        
        # Create ALB Listener (HTTP on port 80)
        self.listener = self.load_balancer.add_listener(
            "AutoChefListener",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            default_action=elbv2.ListenerAction.fixed_response(
                status_code=200,
                content_type="text/plain",
                message_body="AutoChef API Gateway is running!"
            )
        )
        
        # Add routing rules to the listener
        # Route /api/* to Java Service (API Gateway)
        self.listener.add_action(
            "JavaServiceRoute",
            priority=100,
            conditions=[
                elbv2.ListenerCondition.path_patterns(["/api/*"])
            ],
            action=elbv2.ListenerAction.forward([self.java_target_group])
        )
        
        # Route /generate-recipe to Python Service (LLM Service)  
        self.listener.add_action(
            "PythonServiceRoute",
            priority=200,
            conditions=[
                elbv2.ListenerCondition.path_patterns(["/generate-recipe"])
            ],
            action=elbv2.ListenerAction.forward([self.python_target_group])
        )
        
        # Route /health to Python Service for health checks
        self.listener.add_action(
            "PythonHealthRoute",
            priority=300,
            conditions=[
                elbv2.ListenerCondition.path_patterns(["/health"])
            ],
            action=elbv2.ListenerAction.forward([self.python_target_group])
        )
        
        # ========================================
        # ECS Infrastructure - Step 1: Basic Cluster
        # ========================================
        
        # Create ECS Cluster (Fargate mode - serverless containers)
        self.ecs_cluster = ecs.Cluster(
            self, "AutoChefECSCluster",
            vpc=self.vpc,
            cluster_name="autochef-cluster",
            container_insights=True  # Enable monitoring
        )
        
        # ========================================
        # Service Discovery (AWS Cloud Map)
        # ========================================
        
        # Create a private DNS namespace for service discovery
        # Services can find each other using DNS names like: service-name.autochef.local
        self.service_discovery_namespace = servicediscovery.PrivateDnsNamespace(
            self, "AutoChefServiceDiscoveryNamespace",
            name="autochef.local",  # Private DNS namespace
            vpc=self.vpc,
            description="Service discovery namespace for AutoChef microservices"
        )
        
        # ========================================
        # ECS Infrastructure - Step 2: Task Definitions (Container Blueprints)
        # ========================================
        
        # Task Definition for Java Service (Spring Boot API Gateway)
        self.java_task_definition = ecs.FargateTaskDefinition(
            self, "JavaServiceTaskDef",
            memory_limit_mib=1024,  # 1GB RAM
            cpu=512,                # 0.5 vCPU
            family="autochef-java-service"
        )
        
        # Add Java container to the task definition
        self.java_container = self.java_task_definition.add_container(
            "JavaServiceContainer",
            image=ecs.ContainerImage.from_ecr_repository(
                repository=self.java_service_repo,  # Our ECR repo
                tag="latest"
            ),
            environment={
                "LLM_SERVICE_URL": "http://python-service.autochef.local:8000/api/v1/generate-recipe"
            },
            port_mappings=[
                ecs.PortMapping(container_port=8080, protocol=ecs.Protocol.TCP)
            ],
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="java-service",
                log_retention=logs.RetentionDays.ONE_WEEK
            )
        )
        
        # Task Definition for Python Service (FastAPI LLM Service)
        self.python_task_definition = ecs.FargateTaskDefinition(
            self, "PythonServiceTaskDef",
            memory_limit_mib=512,   # 512MB RAM (smaller than Java)
            cpu=256,                # 0.25 vCPU (lighter workload)
            family="autochef-python-service"
        )
        
        # Add IAM permissions for AWS Bedrock access
        # The Python service needs to call Bedrock to generate recipes
        self.python_task_definition.task_role.add_to_principal_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                resources=[
                    "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                    "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
                ]
            )
        )
        
        # Add Python container to the task definition
        self.python_container = self.python_task_definition.add_container(
            "PythonServiceContainer",
            image=ecs.ContainerImage.from_ecr_repository(
                repository=self.python_service_repo,  # Our ECR repo
                tag="latest"
            ),
            port_mappings=[
                ecs.PortMapping(container_port=8000, protocol=ecs.Protocol.TCP)
            ],
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="python-service",
                log_retention=logs.RetentionDays.ONE_WEEK
            )
        )
        
        # ========================================
        # ECS Infrastructure - Step 3: ECS Services (Container Managers)
        # ========================================
        
        # ECS Service for Java Service (Spring Boot API Gateway)
        self.java_service = ecs.FargateService(
            self, "JavaFargateService",
            cluster=self.ecs_cluster,
            task_definition=self.java_task_definition,
            desired_count=1,  # Run 1 container initially
            assign_public_ip=False,  # Private subnets, no public IP needed
            security_groups=[self.ecs_security_group],
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS  # Deploy in private subnets
            ),
            service_name="autochef-java-service"
        )
        
        # Connect Java Service to the Target Group (Load Balancer)
        self.java_service.attach_to_application_target_group(
            self.java_target_group
        )
        
        # ECS Service for Python Service (FastAPI LLM Service)
        self.python_service = ecs.FargateService(
            self, "PythonFargateService",
            cluster=self.ecs_cluster,
            task_definition=self.python_task_definition,
            desired_count=1,  # Run 1 container initially
            assign_public_ip=False,  # Private subnets, no public IP needed
            security_groups=[self.ecs_security_group],
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS  # Deploy in private subnets
            ),
            service_name="autochef-python-service",
            # Enable Service Discovery - register this service with Cloud Map
            cloud_map_options=ecs.CloudMapOptions(
                name="python-service",  # DNS name will be: python-service.autochef.local
                cloud_map_namespace=self.service_discovery_namespace,
                dns_record_type=servicediscovery.DnsRecordType.A,  # A record for IPv4
                dns_ttl=Duration.seconds(10)  # Low TTL for fast DNS updates
            )
        )
        
        # Connect Python Service to the Target Group (Load Balancer)
        self.python_service.attach_to_application_target_group(
            self.python_target_group
        )
