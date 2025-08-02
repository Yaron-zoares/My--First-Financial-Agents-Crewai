# Contributing to Financial Analysis CrewAI System

Thank you for your interest in contributing to our Financial Analysis CrewAI System! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### 1. Fork the Repository
- Fork the repository to your GitHub account
- Clone your fork locally

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8
black --check .
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "feat: add new financial analysis feature"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 📋 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused

### Example Code Style
```python
def calculate_net_present_value(
    cash_flows: List[float], 
    discount_rate: float
) -> float:
    """
    Calculate the Net Present Value of cash flows.
    
    Args:
        cash_flows: List of cash flow amounts
        discount_rate: Annual discount rate (e.g., 0.06 for 6%)
        
    Returns:
        Net Present Value
    """
    npv = 0
    for i, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** i)
    return npv
```

### Commit Message Format
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_financial_analysis.py
```

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Test both success and error cases
- Mock external dependencies

### Example Test
```python
def test_calculate_net_present_value():
    """Test NPV calculation with known values."""
    cash_flows = [1000, 1000, 1000]
    discount_rate = 0.06
    
    npv = calculate_net_present_value(cash_flows, discount_rate)
    
    assert abs(npv - 2673.01) < 0.01
```

## 📚 Documentation

### Code Documentation
- Write clear docstrings for all functions
- Include examples in docstrings
- Document parameters and return values
- Use type hints

### README Updates
- Update README.md for new features
- Include usage examples
- Update installation instructions if needed

## 🔧 Development Setup

### Prerequisites
- Python 3.8 or higher
- pip
- git

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/financial-analysis-crewai.git
cd financial-analysis-crewai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Environment Variables
Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo
```

## 🐛 Reporting Bugs

### Before Reporting
1. Check existing issues
2. Try to reproduce the bug
3. Check the documentation

### Bug Report Template
```markdown
**Bug Description**
Brief description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9.7]
- Package Version: [e.g., 1.0.0]

**Additional Information**
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting
1. Check if the feature already exists
2. Consider if it fits the project scope
3. Think about implementation complexity

### Feature Request Template
```markdown
**Feature Description**
Brief description of the feature

**Use Case**
Why this feature is needed

**Proposed Implementation**
How you think it should be implemented

**Additional Information**
Any other relevant information
```

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] No sensitive data is included

### Pull Request Template
```markdown
**Description**
Brief description of changes

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Other

**Testing**
- [ ] Tests added/updated
- [ ] All tests pass

**Documentation**
- [ ] README updated
- [ ] Code documented
- [ ] No breaking changes

**Additional Notes**
Any additional information
```

## 🏷️ Release Process

### Versioning
We use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] Update version in setup.py
- [ ] Update CHANGELOG.md
- [ ] Create release tag
- [ ] Update documentation

## 🤝 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Be patient with newcomers

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Any other unprofessional conduct

## 📞 Getting Help

- Check the documentation
- Search existing issues
- Ask questions in discussions
- Contact maintainers directly

## 🙏 Acknowledgments

Thank you for contributing to the Financial Analysis CrewAI System! Your contributions help make this project better for everyone.

---

**Note**: This is a living document. Please suggest improvements to these guidelines. 