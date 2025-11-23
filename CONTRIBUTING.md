# Contributing to MadSugu

Thank you for your interest in contributing to MadSugu! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/mad-sugu.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Initialize categories
docker-compose exec backend python init_categories.py
```

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions small and focused

### JavaScript/Svelte (Frontend)
- Use consistent indentation (tabs or 2 spaces)
- Use meaningful variable names
- Keep components small and reusable
- Follow Svelte best practices

## Commit Messages

- Use clear and descriptive commit messages
- Start with a verb in present tense (Add, Fix, Update, Remove)
- Keep the first line under 50 characters
- Provide more details in the body if needed

Examples:
- `Add user profile page`
- `Fix image upload validation`
- `Update README with deployment instructions`

## Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what your PR does and why
3. **Testing**: Describe how you tested your changes
4. **Screenshots**: Include screenshots for UI changes
5. **Breaking Changes**: Highlight any breaking changes

## Testing

Before submitting a PR, make sure:
- [ ] Your code builds without errors
- [ ] All existing tests pass
- [ ] You've added tests for new features
- [ ] You've tested manually in the browser (for frontend changes)

## Areas for Contribution

### High Priority
- Mobile Money payment integration
- Admin dashboard
- Rating and review system
- Email notifications
- SMS notifications

### Medium Priority
- PWA support
- Advanced search features
- Image optimization improvements
- Performance optimizations
- Internationalization (i18n)

### Low Priority
- Analytics dashboard
- Social media sharing
- Dark mode
- Additional themes

## Questions?

If you have questions, feel free to:
- Open an issue
- Contact the maintainers
- Check the documentation

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards others

Thank you for contributing to MadSugu! 🎉
