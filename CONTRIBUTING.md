# 🌱 Detailed Contribution Guidelines

# 🤝 Contribution Guidelines

Thanks for your interest in contributing to GreenEduMap!
Together, let's build an open, green, and sustainable learning ecosystem.

## 💡 Ways to Contribute

1. Bug reports
2. Feature requests
3. Bug fixes and code improvements
4. Documentation improvements
5. Translating documentation into other languages

## ⚙️ Workflow

### 🧭 Environment Setup
1. Fork the repository
2. Clone the forked repository to your local machine
3. Install necessary tools:
   - Appsmith CLI
   - MongoDB Compass (for database testing)
   - VS Code with extensions for JSON/Markdown

### 🧑‍💻 Development
1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/name
   # or
   git checkout -b fix/issue-number
   ```

2. Write code and test:
   - Follow the coding style
   - Test thoroughly before committing
   - Write test cases if necessary

3. Commit changes:
   ```bash
   git add .
   git commit -m "feat/fix: brief description"
   ```

4. Push and create a Pull Request:
   ```bash
   git push origin feature/name
   ```

### 🔎 Review Process
1. Maintainers will review your PR
2. Changes may be requested
3. Once approved, the PR will be merged

## Test

### 🧩 Unit Tests
```bash
npm run test
```

### 🔗 Integration Tests
```bash
npm run test:integration
```

### 🌐 E2E Tests
```bash
npm run test:e2e
```

## 🎨 Style Guide

### 📝 Commit Messages
- feat: Add a new feature
- fix: Fix a bug
- docs: Documentation changes
- style: Formatting, missing semi-colons, etc.
- refactor: Code refactoring
- test: Add test cases
- chore: Update build tasks, package manager, etc.

### 💻 Code Style
- Use 2 spaces for indentation
- Lines should not exceed 80 characters
- Use clear and meaningful variable/function names
- Comment code when necessary