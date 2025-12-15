# Auto-Deploy Assistant - Quick Start Guide

## Project Overview

An intelligent AI-powered deployment tracking system that:
- Automatically monitors GitHub deployments
- Verifies application routes after builds
- Generates AI-powered fix suggestions for errors
- Maintains historical database of all errors
- Sends smart notifications only when needed

## Prerequisites

### Required Accounts
- GitHub account
- Zapier account (free tier)
- Airtable account (free tier)
- OpenAI or Anthropic API key
- Email or Slack for notifications

### Development Tools
- Node.js v16+
- Python 3.8+
- Git

## Quick Setup

### Step 1: Clone and Setup Repository

```bash
# Create new repository or use existing one
git init auto-deploy-assistant
cd auto-deploy-assistant

# Copy the provided files
cp path/to/route_checker.py .
cp path/to/error_analyzer.py .
cp path/to/sample_app.py .
cp path/to/github-workflow-deploy.yml .github/workflows/deploy.yml

# Install dependencies
pip install flask openai  # or: pip install anthropic
```

### Step 2: Setup Airtable

1. **Create Base**: "Deployment Tracker"
2. **Table 1: Deployments**
   - Developer (Single line text)
   - Timestamp (Date with time)
   - Commit Message (Long text)
   - Build Status (Single select: Success/Failed/In Progress)
   - Version (Single line text)

3. **Table 2: Error History**
   - Error Type (Single line text)
   - Code Snippet (Long text)
   - AI Suggestion (Long text)
   - Status (Single select: Open/Resolved)
   - Developer (Single line text)
   - Timestamp (Date with time)

4. **Get API Credentials**
   - Base ID: Found in API docs
   - Table IDs: Found in table URL
   - API Key: From account settings

### Step 3: Configure GitHub Actions

1. Add GitHub Secrets:
   - `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
   
2. Push workflow file:
```bash
git add .github/workflows/deploy.yml
git commit -m "Add deployment workflow"
git push
```

3. Enable GitHub Actions in repository settings

### Step 4: Setup Zapier Workflow

**Create Zap: GitHub → Airtable → Notifications**

1. **Trigger**: GitHub - New Push
2. **Action 1**: Delay - 2 minutes
3. **Action 2**: Webhooks - Get build status from GitHub API
4. **Action 3**: Airtable - Create deployment record
5. **Action 4**: Filter - Only continue if build failed
6. **Action 5**: Airtable - Create error history record
7. **Action 6**: Email/Slack - Send notification

*See full Zapier Configuration Guide for detailed steps*

## Testing Your Setup

### Test 1: Successful Deployment
```bash
# Make a simple change
echo "# Test" >> README.md
git add .
git commit -m "test: successful deployment"
git push
```

**Expected Result**:
- GitHub Actions runs successfully
- Airtable record created with "Success" status
- NO notification sent

### Test 2: Build with Error
```bash
# Create syntax error in sample_app.py
# Remove a colon or add invalid syntax
git add .
git commit -m "test: build error"
git push
```

**Expected Result**:
- GitHub Actions fails
- Error analysis runs
- Airtable error history record created
- Email notification sent with AI suggestions

## File Structure

```
auto-deploy-assistant/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── route_checker.py            # Route verification script
├── error_analyzer.py           # AI error analysis script
├── sample_app.py              # Demo Flask application
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Configuration

### Environment Variables

```bash
# For error analysis (choose one)
export OPENAI_API_KEY="sk-..."
# OR
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Customizing Route Checker

Edit `route_checker.py` to support your framework:
- Flask (Python) - Built-in
- Express.js - Built-in
- Django - Add custom parser
- FastAPI - Add custom parser

## Using the System

### View Deployment Dashboard
1. Open your Airtable base
2. Navigate to "Deployments" table
3. See real-time deployment status

### Check Error History
1. Go to "Error History" table
2. Filter by:
   - Error Type
   - Developer
   - Status (Open/Resolved)
3. Review AI suggestions

### Resolve Errors
1. Check email notification
2. Review AI-generated suggestions
3. Apply suggested fix
4. Mark error as "Resolved" in Airtable

## Advanced Features

### Custom Error Analysis Prompts

Edit `error_analyzer.py` to customize AI prompts:

```python
prompt = f"""Custom analysis prompt here...

ERROR: {error_log}
CODE: {code_snippet}

Return: ...
"""
```

### Add Slack Notifications

In Zapier:
1. Replace "Email by Zapier" with "Slack"
2. Configure channel and message format
3. Include AI suggestions in Slack message

### Deploy Scripts as API

For production use, deploy Python scripts to:
- **AWS Lambda**: Serverless function
- **Vercel**: Serverless API endpoints
- **PythonAnywhere**: Simple Python hosting
- **Heroku**: Full app deployment

## Troubleshooting

### Route Checker Not Finding Routes
```bash
# Test manually
python route_checker.py sample_app.py

# Should output JSON with routes found
```

### Error Analyzer Not Working
```bash
# Check API key
echo $OPENAI_API_KEY

# Test manually
echo "SyntaxError: invalid syntax" | python error_analyzer.py
```

### Zapier Not Triggering
1. Check GitHub webhook settings
2. Verify Zapier is connected to correct repository
3. Test Zap manually in Zapier dashboard
4. Check Zap History for errors

### No Email Notifications
1. Verify email address in Zapier
2. Check spam folder
3. Review Zapier filter conditions
4. Test email action manually

## Monitoring & Analytics

### Key Metrics to Track
- Total deployments
- Success/failure rate
- Average time to resolution
- Most common error types
- Errors by developer

### Create Airtable Views
1. **Recent Deployments**: Last 7 days
2. **Failed Builds**: Status = Failed
3. **Open Errors**: Status = Open
4. **By Developer**: Group by developer name


- **GitHub Actions Docs**: https://docs.github.com/actions
- **Zapier Documentation**: https://zapier.com/help
- **Airtable API**: https://airtable.com/api
- **Anthropic API**: https://docs.anthropic.com



**Built for LD7237 AI Agents Hackathon**
**By Priyadharshini Lavakumar; priyadarshinilavakumar@gmail.com**
**Nikhil Kumar Yerram; Nikhilkumaryerram29@gmail.com**
**Mmaduabuchi Leonard Nwatu; Nwatummaduabuchi@gmail.com**
**Rakesh Babu Kancharla; kancharlarakeshbabu@gmail.com**
**Amrutha Valli Rayana; amrutha2000uk@gmail.com**
*Last updated: 2025*
