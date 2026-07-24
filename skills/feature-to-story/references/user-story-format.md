# User Story Format

> **Supporting reference** for the story-refinement module.
> The primary workflow document is `feature_decomposition_process.md`.

This is the story card schema used by the feature decomposition process.

## Story Structure

Every refined user story should include these core elements:

1. **Title** (3-part template)
2. **Acceptance Criteria**
3. **Files That Will Need Modification** (REQUIRED)
4. **Additional Notes** (optional)

---

## 1. Title (3-Part Template)

```
As a [user type/persona/role],
I want to [do something],
so that I can [get a clear benefit].
```

### Guidelines

✅ **Focus on user needs**, not system behavior
✅ **Avoid technical/system language** — stay user-centered
✅ **Be specific** about the role and benefit

### Examples

❌ **Bad**: "As a user, I want the system to validate my password..."

- Too system-focused ("the system")
- Benefit is missing

✅ **Good**: "As a new user, I want to be notified if my password doesn't meet the criteria, so I can create a secure account."

- User-focused
- Clear action and benefit

---

## 2. Acceptance Criteria

Each criterion should have:

- **A clear heading**
- **A description of a specific scenario**
- **Expected outcome**

### Template

```markdown
## Acceptance Criteria

### [Heading]

[Scenario/Expected Outcome]

### [Heading]

[Scenario/Expected Outcome]
```

### What to Cover

Acceptance criteria should address:

- ✅ **Happy paths** (normal, successful flows)
- ✅ **Failure cases** (what happens when things go wrong)
- ✅ **UX considerations** (user feedback, loading states, etc.)
- ✅ **Compliance or data rules** (validation, business rules)
- ✅ **Edge cases** (empty states, boundary conditions)
- ✅ **Security or access control** (permissions, authorization)

### Best Practices

- **Be specific and testable**: Avoid vague terms like "user-friendly", "fast", "properly"
- **Use plain English**: Non-technical stakeholders should understand
- **Focus on what, not how**: Describe outcomes, not implementation
- **Avoid UI details**: Don't specify colors, exact pixel positions, fonts (unless critical)
- **Use Given/When/Then** (optional but recommended for clarity):

```markdown
### Invalid Email Format

Given a user enters an email without "@" symbol
When they submit the registration form
Then an error message "Please enter a valid email address" is displayed
And the form is not submitted
```

### Examples

#### Example 1: Search Feature

```markdown
## Acceptance Criteria

### Successful Search

When a user enters a search term and clicks "Search", relevant results are displayed with product name, image, and price.

### No Results Found

When a search term yields no results, display a friendly message: "No products found. Try different keywords." with suggestions for popular categories.

### Empty Search

When a user clicks "Search" with an empty input field, display an error message: "Please enter a search term."

### Search Performance

Search results should be displayed within 2 seconds for queries returning up to 1000 results.
```

#### Example 2: User Registration

```markdown
## Acceptance Criteria

### Valid Registration

Given a user provides valid email, password (8+ chars, 1 uppercase, 1 number), and accepts terms
When they submit the registration form
Then their account is created and they receive a confirmation email within 1 minute

### Invalid Email

When a user enters an invalid email format (missing @, invalid domain), an error appears: "Please enter a valid email address" and form submission is blocked.

### Weak Password

When a user enters a password not meeting requirements, display: "Password must be at least 8 characters with 1 uppercase letter and 1 number."

### Duplicate Email

When a user attempts to register with an email already in the system, display: "This email is already registered. Please log in or use a different email."

### Terms Not Accepted

When a user attempts to submit without checking the "Accept Terms" checkbox, display: "You must accept the terms and conditions to register."
```

---

## 3. Files That Will Need Modification (REQUIRED)

This section provides developers with a concrete roadmap of files they'll need to change.

### Template

```markdown
## Files That Will Need Modification

### Frontend (UI):

- **`path/to/component.tsx`** - Description of change
- **`path/to/new-component.tsx`** (NEW) - Description of what this new file does

### Backend (API):

- **`path/to/controller.cs`** - Description of change
- **`path/to/handler.cs`** (NEW) - Description

### Database:

- **`path/to/migration.sql`** (NEW) - Description of schema changes

### Tests:

- **`path/to/test.cs`** - Description of test coverage

### Configuration:

- **`config/settings.json`** - Description of config changes

### Related Implementation Patterns:

Following similar patterns from:

- [Previous similar ticket or feature]
- [Related implementation]
```

### Best Practices

- ✅ **Group files by logical category** (Frontend, Backend, Database, Tests, etc.)
- ✅ **Mark new files with (NEW)**
- ✅ **Be specific about file paths** (use actual project structure)
- ✅ **Include brief description** of what changes are needed
- ✅ **Reference similar implementations** or patterns from codebase
- ✅ **Include test files** (unit, integration, E2E) - testing is not optional
- ✅ **Add implementation notes per file** (optional but helpful):

```markdown
### Backend (API):

- **`src/api/UserController.ts`** - Add registration endpoint and request validation
- **`src/services/EmailService.ts`** (NEW) - Send confirmation emails and handle delivery failures
```

### Example

```markdown
## Files That Will Need Modification

### Frontend (UI):

- **`src/components/SearchBar.tsx`** - Add search input field and button with enter key support
- **`src/pages/SearchResults.tsx`** (NEW) - Display search results with product cards
- **`src/hooks/useSearch.ts`** (NEW) - Custom hook for search API call and state management

### Backend (API):

- **`src/controllers/ProductController.ts`** - Add GET /api/products/search endpoint
- **`src/services/ProductSearchService.ts`** (NEW) - Implement search logic with fuzzy matching

### Database:

- **`migrations/012_add_search_index.sql`** (NEW) - Add full-text search index on product_name and description fields

### Tests:

- **`tests/unit/ProductSearchService.test.ts`** (NEW) - Unit tests for search logic (empty query, special chars, etc.)
- **`tests/integration/ProductController.test.ts`** - Integration tests for search endpoint
- **`tests/e2e/search.spec.ts`** (NEW) - E2E test: user searches, sees results, clicks product

### Related Implementation Patterns:

Following similar patterns from:

- Filter functionality (PROJ-456) - Similar API structure
- Product listing page - Reusing ProductCard component
```

---

## 4. Additional Notes (Optional)

Use this section for:

- **Links to mockups or designs** (Figma, wireframes)
- **References to documentation** (API specs, architecture docs)
- **Dependencies or blockers** (requires feature X to be completed first)
- **Technical considerations** (performance concerns, security notes)
- **Out of scope** (what this story explicitly does NOT include)

### Template

```markdown
## Additional Notes

### Design References

- Figma: [Link to design]
- Mockups: [Link to mockups]

### Dependencies

- Requires PROJ-123 (User authentication) to be completed first
- Needs API key from External Service (Marketing to provide)

### Technical Considerations

- Consider caching search results for 5 minutes to reduce DB load
- Implement rate limiting (max 10 searches per minute per user)

### Out of Scope

- Advanced filters (price range, category) - deferred to PROJ-790
- Search history - deferred to PROJ-791
- Voice search - not planned for this release
```

---

## Complete Example: Registration Story

```markdown
# User Story: User Registration

As a new visitor,
I want to create an account with my email and password,
so that I can access personalized features and save my preferences.

## Acceptance Criteria

### Valid Registration

Given a user provides:

- Valid email (contains @, valid domain)
- Strong password (8+ characters, 1 uppercase, 1 number)
- Accepts terms and conditions

When they submit the registration form
Then:

- Their account is created in the system
- They receive a confirmation email within 1 minute
- They are redirected to the onboarding page

### Invalid Email Format

When a user enters an email without "@" or with invalid domain
Then display error: "Please enter a valid email address"
And prevent form submission

### Weak Password

When a user enters a password not meeting requirements
Then display error: "Password must be at least 8 characters with 1 uppercase letter and 1 number"
And prevent form submission

### Duplicate Email

When a user attempts to register with an email already in the system
Then display error: "This email is already registered. Please log in or reset your password."
And provide link to login page

### Terms Not Accepted

When a user attempts to submit without checking "Accept Terms"
Then display error: "You must accept the terms and conditions"
And prevent form submission

### Confirmation Email

The confirmation email should:

- Include a verification link valid for 24 hours
- Display user's email address
- Provide link to customer support
- Be sent from noreply@company.com

## Files That Will Need Modification

### Frontend (UI):

- **`src/pages/RegistrationPage.tsx`** (NEW) - Registration form with email, password fields, terms checkbox, submit button
- **`src/components/PasswordStrengthIndicator.tsx`** (NEW) - Visual indicator showing password strength
- **`src/utils/validation.ts`** - Add email and password validation functions
- **`src/styles/registration.module.css`** (NEW) - Styling for registration page

### Backend (API):

- **`src/controllers/AuthController.ts`** - Add POST /api/auth/register endpoint
- **`src/services/UserService.ts`** (NEW) - Handle user creation logic
- **`src/services/EmailService.ts`** - Add sendConfirmationEmail method
- **`src/middleware/validation.ts`** - Add registration request validation

### Database:

- **`migrations/008_create_users_table.sql`** (NEW) - Create users table (id, email, password_hash, verified, created_at)
- **`migrations/009_create_verification_tokens.sql`** (NEW) - Create verification_tokens table

### Tests:

- **`tests/unit/validation.test.ts`** - Unit tests for email/password validation
- **`tests/integration/AuthController.test.ts`** (NEW) - Integration tests for registration endpoint
- **`tests/e2e/registration.spec.ts`** (NEW) - E2E test: user registers, verifies email, logs in

### Configuration:

- **`config/email.json`** - Add SMTP settings for confirmation emails
- **`.env.example`** - Add EMAIL_SERVICE_API_KEY

### Related Implementation Patterns:

Following similar patterns from:

- Login functionality (PROJ-234) - Similar validation and auth flow
- Password reset (PROJ-345) - Similar email service usage

## Additional Notes

### Design References

- Figma: https://figma.com/file/abc123 (Registration Flow, Screens 4-6)

### Dependencies

- Email service provider (SendGrid) API key needed from DevOps
- Terms & Conditions page (PROJ-199) must be live before this story

### Technical Considerations

- Passwords must be hashed using bcrypt (cost factor: 10)
- Rate limit registration endpoint to 5 attempts per IP per hour
- Verification tokens should be cryptographically secure (crypto.randomBytes)

### Out of Scope (Future Stories)

- Social login (Google, Facebook) - PROJ-567
- Two-factor authentication - PROJ-568
- Email verification reminder - PROJ-569

### Scope Fit

This story stays focused on account creation and confirmation. Social login, two-factor authentication, and reminder flows remain out of scope.
```

---

## Quick Checklist

Before marking a story as "refined", verify:

- [ ] Title uses 3-part template (As a... I want... so that...)
- [ ] Acceptance criteria cover happy paths, failures, edge cases
- [ ] Acceptance criteria are specific and testable (no vague terms)
- [ ] "Files That Will Need Modification" section is included
- [ ] Files are grouped by category (Frontend, Backend, Database, Tests)
- [ ] New files marked with (NEW)
- [ ] Test coverage is included
- [ ] Story passes INVEST criteria
- [ ] Story is bounded to one focused slice
