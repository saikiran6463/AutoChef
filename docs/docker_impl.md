# 1. Navigate to project
cd /Users/saikiran/Projects/AutoChef

# 2. Export AWS credentials (once per terminal session)
eval $(aws configure export-credentials --format env)

# 3. Start everything
docker-compose up --build -d

# 4. Test integration
curl -X POST http://localhost:8080/api/v1/generate-recipe \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I have pasta and mushrooms"}'

# 5. View logs if needed
docker-compose logs -f

# 6. When done
docker-compose down

## Side Notes:
docker compose yaml file is used only for local testing . Inorder to deploy them in the ECS we need individual service images pushed to the ECR where ECS creates its specific task defination  and runs on the containers.