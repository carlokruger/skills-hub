# Story Splitting Patterns

> **Supporting reference** for the story-refinement module.
> The primary workflow document is `feature_decomposition_process.md`.

This is a supporting reference used by the feature decomposition process.

## When to Split a User Story

A story needs splitting if:

- **Still too vague**: Scope, dependencies, or open questions are not explicit enough
- **Bundles too much**: Multiple outcomes or handoffs are trapped in one story
- **Too complex**: Multiple features bundled together
- **Violates INVEST-style readiness**: Not Independent, Negotiable, Valuable, Explicit, Small, or Testable

## 8 Primary Splitting Patterns

### 1. By Operations (CRUD)

**Pattern**: Split by Create, Read, Update, Delete operations

**When to use**: Story involves managing data entities

**Example**:

- ❌ **Too Large**: "As a user, I want to manage products so that I can keep my catalog up to date"
- ✅ **Split**:
  1. "As a user, I want to create new products..."
  2. "As a user, I want to view product details..."
  3. "As a user, I want to edit existing products..."
  4. "As a user, I want to delete products..."

**Benefits**:

- Clear, distinct functionality per story
- Each operation can be developed independently
- Easy to prioritize (e.g., Create + Read first, Update + Delete later)

---

### 2. By Parameters/Data Types

**Pattern**: Split by different input types, search criteria, or data variations

**When to use**: Story handles multiple types of inputs or searches

**Example**:

- ❌ **Too Large**: "As a user, I want to search for products so that I can find what I'm looking for"
- ✅ **Split**:
  1. "As a user, I want to search products by name..."
  2. "As a user, I want to search products by price range..."
  3. "As a user, I want to search products by category..."
  4. "As a user, I want to search products by color..."

**Benefits**:

- Incremental feature delivery
- Can prioritize most common search types first
- Easier testing (one parameter type per story)

---

### 3. By Workflow Steps

**Pattern**: Split into sequential steps of a process

**When to use**: Story describes a multi-step workflow or user journey

**Example**:

- ❌ **Too Large**: "As a shopper, I want to buy goods so that I can receive my items"
- ✅ **Split**:
  1. "As a shopper, I want to review my order summary..."
  2. "As a shopper, I want to enter payment information..."
  3. "As a shopper, I want to receive order confirmation..."
  4. "As a shopper, I want to receive shipping notification..."

**Benefits**:

- Each step is a vertical slice
- Can deliver value incrementally (e.g., review first, then payment)
- Maps well to user journey

---

### 4. By Happy/Unhappy Path

**Pattern**: Split success scenarios from error/edge cases

**When to use**: Story has complex error handling or multiple failure scenarios

**Example**:

- ❌ **Too Large**: "As a user, I want to log in so that I can access my account"
- ✅ **Split**:
  1. "As a user, I want to log in with valid credentials..."
  2. "As a user, I want to reset my password if forgotten..."
  3. "As a user, I want to recover my username if forgotten..."
  4. "As a user, I want to unlock my account after too many failed attempts..."

**Benefits**:

- Deliver happy path first (80% of usage)
- Defer complex error handling
- Easier to validate and test

---

### 5. By Business Rules

**Pattern**: Split by different rules, constraints, or conditions

**When to use**: Story involves multiple business rules or conditional logic

**Example**:

- ❌ **Too Large**: "As a customer, I want to process my order so that I can complete my purchase"
- ✅ **Split**:
  1. "As a customer, I want to process orders above minimum order value..."
  2. "As a customer, I want to see error if order below minimum..."
  3. "As a customer, I want to see geographic shipping restrictions..."
  4. "As a customer, I want to see timeout warning for pending payment..."

**Benefits**:

- Each rule can be implemented independently
- Can prioritize most common rules first
- Reduces complexity per story

---

### 6. By Platform/Device

**Pattern**: Split by desktop, mobile, tablet, or different browsers

**When to use**: Story needs to work across multiple platforms with different UX

**Example**:

- ❌ **Too Large**: "As a user, I want to view my order status so that I can track my delivery"
- ✅ **Split**:
  1. "As a user, I want to view order status on desktop..."
  2. "As a user, I want to view order status on Android..."
  3. "As a user, I want to view order status on iOS..."

**Benefits**:

- Can deliver to one platform first
- Platform-specific optimizations per story
- Parallel development possible

---

### 7. By None/One/Many (Spike Pattern)

**Pattern**: Spike to investigate → Implement first → Implement rest using template

**When to use**: Story involves repeating similar implementations or unknowns

**Example**:

- ❌ **Too Large**: "As a merchant, I want to accept all major credit cards so that I can process payments"
- ✅ **Split**:
  1. "Spike: Research credit card integration options and select provider" (investigation)
  2. "As a merchant, I want to accept Visa payments..." (first implementation)
  3. "As a merchant, I want to accept MasterCard/Discover/Amex..." (template reuse)

**Benefits**:

- Reduces uncertainty through spike
- First implementation creates template
- Remaining implementations faster (reuse pattern)

**Note**: This pattern explicitly includes a spike (research/investigation story) with no production code

---

### 8. By Complexity (Simple First, Optimize Later)

**Pattern**: Build basic version first, then add performance/polish

**When to use**: Story has simple core functionality plus complex optimizations

**Example**:

- ❌ **Too Large**: "As a user, I want lightning-fast search with autocomplete, typo correction, and advanced filtering"
- ✅ **Split**:
  1. "As a user, I want to search by exact keyword match..." (simple)
  2. "As a user, I want to see autocomplete suggestions..." (enhancement)
  3. "As a user, I want search to handle typos..." (optimization)
  4. "As a user, I want advanced filtering options..." (enhancement)

**Benefits**:

- Deliver working feature quickly
- Defer optimization until needed
- Gather user feedback on basic version first

**Motto**: "Make it work, then make it better"

---

## Splitting Process

1. **Identify the pattern**: Which splitting pattern applies to this story?
2. **Propose the split**: Break into 3-8 smaller stories
3. **Validate each story**: Ensure each passes INVEST criteria
4. **Define sequence**: Recommend implementation order based on dependencies/risk
5. **Preserve value**: Each story should deliver some value independently

## When NOT to Split

Don't split if:

- Story is already one focused, independently testable slice
- Splitting would create trivial stories that provide no meaningful standalone value
- Split stories would have tight dependencies (consider combining instead)
- You're in "Chaotic" domain (Cynefin framework) - put out the fire first

**Important**: If you have many dependent stories, they're probably too small and should be combined.

## Combining Multiple Patterns

You can apply multiple patterns to the same story:

**Example**: "Manage user accounts across platforms"

1. First split by **Platform**: Desktop vs Mobile
2. Then split by **Operations**: Create, Edit, Delete
3. Then split by **Happy/Unhappy Path**: Success vs Error handling

This gives you a grid of stories: Desktop Create (Happy), Desktop Create (Error), Mobile Create (Happy), etc.

## Validation Checklist

After splitting, verify:

- [ ] Each story passes INVEST criteria
- [ ] Each story delivers independent value
- [ ] Stories are bounded to focused, independently testable slices
- [ ] Implementation order is clear (which story first?)
- [ ] No story is too trivial to stand on its own
- [ ] Dependencies are minimized

## Example: Complete Splitting Exercise

### Original (Too Large)

"As a shopper, I want to search for products, filter by category, sort by price, add to cart, and checkout so that I can buy items easily."

**Scope signal**: Clearly bundles several different outcomes and handoffs

### Analysis

This story bundles:

- Search functionality
- Filtering
- Sorting
- Cart management
- Checkout process

**Pattern to apply**: By Workflow Steps (user journey)

### Split Stories

1. **Search**: "As a shopper, I want to search for products by keyword, so that I can quickly find items I'm interested in."

2. **Filter**: "As a shopper, I want to filter products by category, so that I can narrow results to the most relevant items."

3. **Sort**: "As a shopper, I want to sort products by price, so that I can easily compare within my budget."

4. **Add to Cart**: "As a shopper, I want to add products to my cart, so that I can save them for purchase."

5. **Checkout**: "As a shopper, I want to checkout, so that I can complete my purchase and receive my items."

### Further Splitting (Checkout is still too large)

Apply **By Workflow Steps** to Checkout:

5a. **Review Order**: "As a shopper, I want to review my order summary before paying..."

5b. **Payment**: "As a shopper, I want to enter payment information securely..."

5c. **Confirmation**: "As a shopper, I want to receive order confirmation with details..."

### Final Result

7 stories, each bounded, each delivering value, each testable independently.

**Recommended implementation order**:

1. Search (enables discovery)
2. Add to Cart (enables selection)
3. Review Order (enables purchase intent)
4. Payment (enables transaction)
5. Confirmation (completes flow)
6. Filter (enhancement)
7. Sort (enhancement)

## Tips and Tricks

### Start with Value

Always ask: "What's the minimum valuable increment we can deliver?"

### Think Vertical, Not Horizontal

❌ Bad: "Story 1: Database schema, Story 2: API, Story 3: UI"
✅ Good: Each story includes DB + API + UI for one feature

### Use Spikes Wisely

If you don't know how to implement something, create a spike story to research, then implement

### Avoid the "Iceberg Story"

If a story looks small but has huge hidden complexity, split by complexity (simple first)

### Remember the User

Every split story should still be valuable to an end user (not just a technical task)
