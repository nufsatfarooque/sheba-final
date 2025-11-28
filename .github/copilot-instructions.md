# Copilot Instructions for Sheba Final

## Project Overview
Sheba Final is a hackathon project focused on [project domain - to be updated based on actual implementation]. This is a rapid development project with emphasis on quick iteration and feature delivery.

## Architecture & Structure
*Note: Update this section once the project structure is established*

```
sheba-final/
├── src/                # Main source code
├── public/             # Static assets (if web-based)
├── docs/               # Documentation
├── tests/              # Test files
└── config/             # Configuration files
```

## Development Workflow

### Quick Start Commands
```bash
# Setup (update based on actual tech stack)
npm install              # or pip install -r requirements.txt
npm run dev             # or python main.py

# Testing (update based on testing framework)
npm test                # or pytest
npm run test:watch      # for continuous testing
```

### Build & Deployment
```bash
# Build for production
npm run build           # or appropriate build command

# Run production build locally
npm start               # or production server command
```

## Key Patterns & Conventions

### Code Organization
- Follow hackathon rapid development principles
- Prioritize working features over perfect architecture
- Keep components modular for easy iteration
- Use clear, descriptive naming for quick understanding

### Configuration Management
- Environment variables in `.env` files
- Separate development and production configs
- API keys and secrets through environment variables

### Error Handling
- Implement basic error boundaries/handling
- Log errors appropriately for debugging
- Graceful degradation where possible

## Integration Points
*Update based on actual integrations*

### External APIs
- Document any third-party service integrations
- Include authentication patterns
- Note rate limiting considerations

### Database/Storage
- Document data models and relationships
- Include migration patterns if applicable
- Note any data seeding requirements

## Hackathon-Specific Guidelines

### Development Priorities
1. **MVP First**: Focus on core functionality before polish
2. **Demo-Ready**: Ensure features work reliably for demonstration
3. **Time Management**: Timebox features to maintain project velocity
4. **Documentation**: Keep README updated with setup instructions

### Code Quality Balance
- Readable code over complex optimization
- Working features over comprehensive testing
- Clear variable/function names for team collaboration
- Comment complex business logic and workarounds

### Team Collaboration & Git Workflow
- **Branch Strategy**: Use feature branches (`feature/feature-name`) for development
- **Commit Convention**: Follow conventional commits format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for code refactoring
  - `test:` for adding tests
  - Example: `feat: add user authentication flow`
- **Pull Request Process**: 
  - Create PR from feature branch to `main`
  - Add descriptive title and description
  - Request review from at least one team member
  - Squash commits when merging to keep history clean
- **Protect Main Branch**: No direct commits to `main`, all changes via PR

## Common Commands & Debugging

### Development Tools
```bash
# Linting (if configured)
npm run lint            # or flake8, black, etc.

# Format code (if configured)  
npm run format          # or prettier, black --format

# View logs
tail -f logs/app.log    # or appropriate log viewing
```

### Troubleshooting
- Check environment variable setup first
- Verify all dependencies are installed
- Clear cache/node_modules if issues persist
- Check network connectivity for API calls

## GitHub Workflow Guide

### Initial Repository Setup
```powershell
# Initialize git and create initial commit
git init
git add .
git commit -m "chore: initial project setup"

# Add remote repository (replace with your repo URL)
git remote add origin https://github.com/yourusername/sheba-final.git
git branch -M main
git push -u origin main
```

### Daily Development Workflow
```powershell
# 1. Update your local main branch
git checkout main
git pull origin main

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and commit frequently
git add .
git commit -m "feat: add specific feature description"

# 4. Push branch to remote
git push -u origin feature/your-feature-name

# 5. Create Pull Request on GitHub
# 6. After PR approval and merge, clean up
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

### Working with Issues
- Create GitHub Issues for each feature/bug
- Reference issues in commits: `feat: add login (#5)`
- Link PRs to issues they resolve: `Closes #5`
- Use labels: `bug`, `enhancement`, `documentation`, `priority-high`

### Branch Naming Conventions
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/what-changed` - Documentation updates
- `refactor/component-name` - Code refactoring
- `test/what-tested` - Adding tests

### Handling Merge Conflicts
```powershell
# Update your branch with latest main
git checkout feature/your-branch
git fetch origin
git merge origin/main

# Fix conflicts in files, then:
git add .
git commit -m "merge: resolve conflicts with main"
git push
```

### Important Git Commands
```powershell
# Check status
git status

# View commit history
git log --oneline --graph --all

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard origin/main

# Stash changes temporarily
git stash
git stash pop

# Create tag for releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Files to Update When Adding Features
- `README.md` - Update setup and usage instructions
- `package.json`/`requirements.txt` - Add new dependencies
- `.env.example` - Document new environment variables
- This file - Update patterns and conventions as they emerge
- `CHANGELOG.md` - Document changes for each version

---

*This file should be updated as the project evolves. Focus on documenting actual patterns used in the codebase rather than aspirational practices.*