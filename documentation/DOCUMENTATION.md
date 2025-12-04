# Unity Documentation Index

Complete guide to all Unity library documentation.

## 📚 Documentation Files

### Getting Started

**[GUIDE.md](GUIDE.md)** - Start here!
- What is Unity?
- Installation instructions
- Basic concepts (units, quantities, scalars vs arrays)
- Your first conversion and calculation
- Real-world examples
- Common workflows
- Troubleshooting

**[README.md](README.md)** - Overview
- Features summary
- Quick start examples
- Supported units overview
- Installation and testing instructions

### Reference & API

**[API_REFERENCE.md](API_REFERENCE.md)** - Quick lookup
- Function signatures and parameters
- Return types and exceptions
- Quick examples for each function/method
- Common unit strings reference
- Type hints guide
- One-page reference

**[reference.md](reference.md)** - Detailed API documentation
- Core functions (`conv`, `valid`, `parse_unit`)
- Quantity class comprehensive documentation
- Supported units tables
- Compound unit syntax with examples
- Usage guides with code
- Real-world examples

### Specialized Guides

**[ARRAYS.md](ARRAYS.md)** - Array operations guide
- Creating array quantities (from lists, numpy arrays)
- Accessing array values (indexing, slicing)
- Array arithmetic (element-wise, broadcasting)
- Unit conversions with arrays
- Array formatting
- Advanced numpy operations
- Broadcasting rules
- Performance tips
- Common patterns
- Real-world examples

## 📖 Documentation by Use Case

### "I want to learn the basics"
1. Read: [GUIDE.md](GUIDE.md) - Basic Concepts section
2. Run: `python examples/demo.py`
3. Test: `python testing/test_quantity_ops.py`

### "I need to convert a single value"
1. Check: [API_REFERENCE.md](API_REFERENCE.md) - `Quantity` class
2. Example: [GUIDE.md](GUIDE.md) - Your First Conversion
3. Reference: [reference.md](reference.md) - Unit Conversion section

### "I need to work with multiple values"
1. Read: [ARRAYS.md](ARRAYS.md) - Creating Array Quantities
2. Examples: [ARRAYS.md](ARRAYS.md) - Real-World Examples
3. Run: `python examples/array_demo.py`
4. Test: `python testing/test_quantity_arrays.py`

### "I need to perform calculations"
1. Check: [GUIDE.md](GUIDE.md) - Your First Calculation
2. Lookup: [API_REFERENCE.md](API_REFERENCE.md) - Arithmetic Operators
3. Reference: [reference.md](reference.md) - Arithmetic Operations

### "I'm looking for specific information"
1. Quick lookup: [API_REFERENCE.md](API_REFERENCE.md) - One-page reference
2. Detailed info: [reference.md](reference.md) - Comprehensive documentation
3. Array-specific: [ARRAYS.md](ARRAYS.md) - Array operations guide

### "I want to see working examples"
- Basic: `examples/demo.py`
- Arrays: `examples/array_demo.py`
- Tests: `testing/test_quantity_*.py`

## 📋 Quick Cheat Sheet

### Imports
```python
from unity.quantity import Quantity
from unity.core import conv, valid
```

### Create Quantities
```python
scalar = Quantity(10, "m")
array = Quantity([1, 2, 3], "m")
```

### Convert Units
```python
q_meters = Quantity(5, "km").to("m")
```

### Perform Calculations
```python
velocity = distance / time
force = mass * acceleration
```

### Access Elements
```python
first = array[0]      # Scalar
slice = array[1:4]    # Array
```

### Format Output
```python
print(q.format())     # Auto-format
print(q.format(".2f"))  # Custom format
```

## 🔍 What's Documented

### Core Features
- ✅ Unit conversion (scalar and array)
- ✅ Arithmetic operations with units
- ✅ Dimensional analysis and validation
- ✅ Array operations (element-wise, broadcasting)
- ✅ Indexing and slicing
- ✅ Formatting with smart magnitude handling

### Supported Units
- ✅ Base SI units (m, kg, s)
- ✅ Prefixed units (mm, cm, km, etc.)
- ✅ Derived units (N, Pa, J, W, Hz)
- ✅ Custom compound units

### Examples Provided
- Basic scalar operations
- Array element-wise operations
- Broadcasting examples
- Physics calculations
- Unit conversions
- Data processing

## 📚 Documentation Structure

```
Unity Package
├── GUIDE.md                    ← START HERE
├── README.md                   ← Overview
├── API_REFERENCE.md            ← Quick lookup
├── reference.md                ← Detailed API
├── ARRAYS.md                   ← Array operations
├── DOCUMENTATION.md            ← This file
├── examples/
│   ├── demo.py                ← Basic examples
│   └── array_demo.py          ← Array examples
├── testing/
│   ├── test_quantity_ops.py   ← Operation tests
│   ├── test_quantity_format.py ← Format tests
│   └── test_quantity_arrays.py ← Array tests
└── src/unity/
    ├── quantity.py            ← Main class
    ├── core.py                ← Core functions
    └── db.py                  ← Unit database
```

## 🎯 Learning Path

### For Beginners
1. Read: [GUIDE.md](GUIDE.md)
2. Try: `python examples/demo.py`
3. Experiment: Simple conversions and calculations
4. Reference: [API_REFERENCE.md](API_REFERENCE.md) when needed

### For Intermediate Users
1. Read: [reference.md](reference.md)
2. Try: `python examples/array_demo.py`
3. Experiment: Array operations and broadcasting
4. Reference: [ARRAYS.md](ARRAYS.md) for details

### For Advanced Users
1. Study: [ARRAYS.md](ARRAYS.md) - Advanced section
2. Examine: Test files for usage patterns
3. Check: Source code for implementation details
4. Integrate: With your numpy-based projects

## 📝 Documentation Conventions

### Code Examples
- Single value examples use scalars
- Multiple value examples use arrays
- Comments explain what each line does

### Function Signatures
- Parameters listed in order
- Type hints included
- Return types specified

### Unit Strings
- Spaces separate different units
- Exponents follow unit name (e.g., `m2`)
- Negative exponents for division (e.g., `s-1`)

### Examples Format
```python
# Input
code_here

# Output
Expected result shown as comment
```

## ❓ FAQ

**Q: Which document should I start with?**
A: Start with [GUIDE.md](GUIDE.md) for a comprehensive introduction.

**Q: Where do I find the API?**
A: [API_REFERENCE.md](API_REFERENCE.md) for quick lookup, [reference.md](reference.md) for details.

**Q: How do I work with arrays?**
A: See [ARRAYS.md](ARRAYS.md) for comprehensive array operations guide.

**Q: Are there working examples?**
A: Yes! Check `examples/demo.py` and `examples/array_demo.py`.

**Q: How do I run tests?**
A: `python testing/test_quantity_ops.py` and `python testing/test_quantity_arrays.py`.

## 📞 Support Resources

- **Working Examples**: `examples/` directory
- **Test Suite**: `testing/` directory
- **Source Code**: `src/unity/` directory
- **Documentation**: All `.md` files in root directory

## 🔗 Document Links by Feature

### Unit Conversion
- [GUIDE.md - Your First Conversion](GUIDE.md#your-first-conversion)
- [API_REFERENCE.md - conv()](#) and [to()](#)
- [reference.md - Unit Conversion section](#)

### Arithmetic
- [GUIDE.md - Your First Calculation](GUIDE.md#your-first-calculation)
- [API_REFERENCE.md - Arithmetic Operators](#)
- [reference.md - Arithmetic Operations](#)

### Arrays
- [ARRAYS.md - Creating Array Quantities](#)
- [ARRAYS.md - Array Arithmetic](#)
- [API_REFERENCE.md - Examples - Physics Calculation](#)

### Indexing
- [ARRAYS.md - Accessing Array Values](#)
- [API_REFERENCE.md - __getitem__()](#)

### Formatting
- [GUIDE.md - Formatting Scalars/Arrays](#)
- [API_REFERENCE.md - format()](#)
- [reference.md - format() method](#)

## 📊 Documentation Statistics

- **4 Main Documentation Files**: README, GUIDE, reference, API_REFERENCE
- **1 Specialized Guide**: ARRAYS
- **2 Example Scripts**: demo, array_demo
- **3 Test Suites**: ops, format, arrays
- **100+ Code Examples**: Throughout documentation
- **20+ Real-World Examples**: Physics, engineering, data processing

## 🎓 Recommended Reading Order

1. **Quick Start** (15 min)
   - [GUIDE.md - Basics](GUIDE.md)
   - [README.md](README.md)

2. **First Project** (30 min)
   - [GUIDE.md - Examples](GUIDE.md#real-world-examples)
   - Run: `python examples/demo.py`

3. **Reference** (30 min)
   - [API_REFERENCE.md](API_REFERENCE.md)
   - [reference.md](reference.md)

4. **Arrays** (30 min)
   - [ARRAYS.md](ARRAYS.md)
   - Run: `python examples/array_demo.py`

5. **Deep Dive** (60 min+)
   - Source code in `src/unity/`
   - Test files in `testing/`
   - Explore advanced patterns

## ✅ Verification Checklist

After reading the documentation, you should be able to:

- [ ] Create scalar quantities
- [ ] Create array quantities from lists
- [ ] Convert between units
- [ ] Perform arithmetic with units
- [ ] Index and slice arrays
- [ ] Use broadcasting
- [ ] Format output
- [ ] Validate unit compatibility
- [ ] Handle errors gracefully

If you can do all these, you're ready to use Unity!

## 📄 License

All documentation is provided as part of the Unity package. See LICENSE file for details.

---

**Last Updated**: December 2024
**Version**: 1.0
**Library**: Unity Unit Conversion System

