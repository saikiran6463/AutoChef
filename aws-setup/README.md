# AWS Setup Files

This directory contains AWS configuration files for the AutoChef project.

## Files

### `autochef-bedrock-policy.json`
IAM policy that grants minimal permissions for AutoChef to access AWS Bedrock Claude models.

**Usage:**
- This policy was created in AWS Console as `AutoChefBedrockPolicy`
- Attached to IAM user: `autochef-bedrock-user`
- Grants permissions for: `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`
- Restricted to: Claude 3 Haiku and Sonnet models only

**For new developers:**
1. Create IAM user in AWS Console
2. Create policy using this JSON content
3. Attach policy to user
4. Generate Access Keys for local development

See `/BEDROCK_INTEGRATION_PHASE1.md` for complete setup instructions.