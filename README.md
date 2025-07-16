# HonuLabs CLI

The HonuLabs CLI is a comprehensive tool that allows you to plan and deploy your business ideas with minimal effort. HonuLabs creates a complete business infrastructure from scratch, handling all organizational heavy lifting so you can focus on building your product without worrying about setup complexities.

## What HonuLabs Does for You

HonuLabs automatically sets up and manages:

- **Infrastructure**: Complete technical foundation for your business
- **Landing page**: Professional site to capture early customer interest
- **Payment processing**: Integrated payment solutions
- **Analytics**: Comprehensive tracking and monitoring
- **Development environment**: Ready-to-code application template

### Included Services

- **Supabase**: Backend database and authentication
- **Vercel**: Frontend hosting and deployment
- **Stripe**: Payment processing
- **Google Analytics**: User behavior tracking
- **Google Tag Manager**: Marketing analytics
- **HonuLabs Dashboard**: Monitor key business metrics

## Prerequisites

- Python 3.8 or higher
- Poetry package manager
- Git
- GitHub account
- Active internet connection

## Installation

Install the CLI by cloning the HonuLabs repository:

```bash
git clone https://github.com/honu-ai/honulabs
cd honulabs
poetry install
```

## Quick Start

### 1. Enter the HonuLabs CLI Environment

```bash
poetry run python -m cli
```

### 2. Login to Your Account

You should have received HonuLabs account credentials from our team. Use the login command and follow the on-screen instructions:

```bash
> login
```

You'll be presented with a link to click or copy into your browser. Select your organization if you own multiple organizations. After successful login, you'll see a success screen. Return to the CLI and wait for token verification to complete.

### 3. Explore Available Commands

To see all available tools, use:

```bash
> help
```

or

```bash
> ?
```

## Creating Your Business

### Step 1: Generate a Project

Projects are containers for your business. Each project maps resources to a single business entity. You can create multiple projects, but we recommend one business per project for optimal organization.

Create a new project:

```bash
> create_project
```

Manage existing projects:

```bash
> list_projects    # View all projects
> delete_project   # Remove a project
```

### Step 2: Generate a Business Idea (Optional)

If you don't have a business idea yet, use our AI-powered idea generator:

```bash
> new_business_idea
```

This process will:

- Research industry challenges and market gaps
- Guide you through idea selection
- Take approximately 2-3 minutes per step
- Automatically redirect you to business plan generation

**Note**: If you already have an idea, skip this step and go directly to Step 3.

### Step 3: Generate Your Business Model

This step creates a comprehensive business model based on your responses to targeted questions designed to capture your business intent.

```bash
> generate_business_plan
```

The system will research and generate the following components:

- **Problem definition**: Clear articulation of the problem you're solving
- **Competitor analysis**: Detailed competitive landscape
- **Unique value proposition**: What sets you apart
- **Target market analysis**: Who your customers are
- **Ideal customer profile**: Detailed buyer personas
- **Branding details**: Visual and messaging guidelines
- **Market positioning**: How you fit in the market
- **Product pricing strategy**: Revenue model and pricing tiers
- **MVP sprint plan**: Step-by-step development roadmap

During this process, you'll see progress indicators such as:

```
Defining business problem...
Conducting target market research...
Developing pricing strategy...
Generating the base business plan...
Generating branding components...
Generating website components...
Generating website privacy policy...
Generating website terms of service...
Generating the full business plan...
Generating User Persona...
Analyzing jobs to be done for an MVP...
Generating User Journey mapping...
Generating User Journey flow...
Generating MVP Framework...
Determining required integrations...
Generating MVP Sprint Plan...
```

You'll receive both a comprehensive business plan and an abbreviated executive summary. The system will automatically guide you through the steps, taking approximately 30-40 minutes to complete the process and asking you questions throughout.

## Deployment

### Deploy Your Landing Page

Once you're satisfied with your business plan, deploy a professional landing page with integrated waitlist functionality:

```bash
> deploy_app
```

This command will:

- Deploy a landing page at `<idea_name>.honulabs.xyz`
- Set up Google Analytics and Tag Manager for tracking
- Configure Supabase and Vercel infrastructure
- Create a GitHub repository with a development template
- Return the live URL for immediate access

### Invite Yourself to the Repository

To start developing your application, you need access to the created repository:

```bash
> invite_to_repo
```

This will:

- Ask you to select your project repository
- Request your GitHub username
- Send you an email invitation from the HonuLabs bot

## Development Workflow

### Setting Up Your Local Environment

Clone and set up your project repository:

```bash
git clone <your_project_repository>
cd <your_project_repository>
make run-dev
```

This spins up a local containerized development environment using Docker Compose, allowing you to start coding immediately.

### Execute the First Sprint in Cursor

1. **Attach the relevant files to your prompt**: We have prepared an additional execution guide you can attach to your prompt to make sure that the LLM has enough context when performing the tasks listed in each sprint. This will be in the project management folder in the repository.

2. **Use the following prompt to execute the first sprint**:

```
You are executing Sprint 1 in a structured multisprint development workflow. Review all the task listed in @sprint-1.md and the start executing them in order making sure to follow the @execution-guide.md Once you completed the sprint report to the user and them ask them to double check all the exeptance criteria are being fulfilled. Once you completed the sprint report to the user and them ask them to double check all the expectance criteria are being fulfilled.
```

### 🔄 Execute Subsequent Sprints

For sprints after the first:

1. **Locate the log file** from the previous sprint at `./log/sprint-{sprint id}-logs/log.md`
2. **Include this log file** in the context for the next sprint execution
3. **Use the following prompt**:

```
You are executing Sprint 2 in a structured multisprint development workflow. You can find the logs from the previews sprint @log.md Review all the task listed in @sprint-2.md and then start executing them in order making sure to follow the @execution-guide.md Once you completed the sprint report to the user and them ask them to double check all the expectance criteria are being fulfilled.
```

### ✅ Verify Acceptance Criteria

After each sprint:

1. **Review and confirm** all acceptance criteria have been fulfilled
2. **If criteria remain unfulfilled**, unmark them in the sprint document
3. **Return the document to the agent** with this prompt:

```
The user has reviewed the task and have ticked the acceptance criteria that have been fulfilled. Review the file and complete any outstanding acceptance criteria. Make sure to follow the @execution-guide.md when you are completing those.
```

### Deploying Updates

To deploy your application updates:

1. **Commit and push** your code to the repository
2. **Return to the CLI** and run:

    ```bash
    > deploy_app
    ```

This creates a continuous development loop: **Code in editor → Push to repo → Deploy with CLI**

## HonuLabs MCP Server Integration

HonuLabs provides a Model Context Protocol (MCP) server that integrates with AI development tools like Claude Desktop or Cursor. This allows you to chat with AI about your business and gain insights.

### MCP Server Capabilities

- **Read business information**: Access all your business data and metrics
- **Update business information**: Modify business parameters and settings
- **Project-specific servers**: Each project has its own dedicated MCP server

### Connect to Your Project's MCP Server

Generate the connection configuration:

```bash
> mcp_config_string
```

Select your project from the list, and you'll receive a connection string to add to your AI development tool's configuration.

## Command Reference

| Command | Description |
|---------|-------------|
| `login` | Authenticate with your HonuLabs account |
| `help` or `?` | Show available commands |
| `create_project` | Create a new business project |
| `list_projects` | View all your projects |
| `delete_project` | Remove a project |
| `new_business_idea` | Generate AI-powered business ideas |
| `generate_business_plan` | Create comprehensive business model |
| `deploy_app` | Deploy landing page and infrastructure |
| `invite_to_repo` | Get access to your project repository |
| `mcp_config_string` | Generate MCP server connection config |

## Troubleshooting

### Common Issues

**Authentication Problems**
- Ensure you have valid credentials from the HonuLabs team
- Check your internet connection
- Try logging out and logging back in

**Deployment Failures**
- Verify your project has a complete business plan
- Check that all required services are properly configured
- Contact support if issues persist

**Repository Access Issues**
- Ensure you're using the correct GitHub username
- Check your email for the invitation
- Verify you have the necessary permissions

## Support and Documentation

For additional help and detailed guides:

- Check our comprehensive documentation at [docs.honulabs.com](https://docs.honulabs.com)
- Contact support through the HonuLabs dashboard
- Join our developer community on Discord
- Email support: support@honulabs.com

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

We welcome contributions! Please see our Contributing Guidelines for more information.

---

**Ready to build your next big idea?** Start with `poetry run python -m cli` and let HonuLabs handle the infrastructure while you focus on what matters most—bringing your vision to life.