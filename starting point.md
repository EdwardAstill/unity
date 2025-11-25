this is to be used for units
capcailities: converte between units (in the process validate unit combinations e.g. N can be convertied to kPa m^2 (with a conversion factor of 1000))
i plat to use this like so

## Pure conversion - not sure about this should eb possible need to add a meethod to int and float clas
ideally:
7834.2("N","kPa m2")
likely:
7834.2.conv("N","kPa m2")
or
conv(7834.2,"N","kPa m2")

this will result in 7.8324 (both numbers are integers or floats)

## Quantity objects
quantity object like pint also exist
where there si a magnitude and units
q(7834.2,"N")

some dictionaries will stroe conversion between base units

```python
weight_dict = {"mg":0.001,"g":1,"kg":1000,"t":1000000}
```
other dictionaries will store equivalents
```python
{"N":"kg m s-2"}
```


primary units:
- length
- mass
- time

need to keep track of exponents and 

ultimatesly there will be a middle man ,this is what i will convert both units i am converting between into and ratioing their conversion factor wiill give me the conversion factor between them.


## Example 1 explanation and mg -> kg
lets use the simple logic of how the script will work to convert mg to kg:
the intermediary is gram so i have to see how many grams are in a mg and how many grams are in a kg.
starting with a dictionary for mg (every unit starts with a dictionary that is created from the string)
in this dictionary we have the unit and the exponent
```python
from_dict = {"mg":1}
```
next we need to convert this to grams, because the exponent is one we just do (.001/1)^1 that is
```python
(weight_dict["mg"]/weight_dict["g"])**exponent
```
not sure about what do do here like how i ant to store it
```python
from_dict_conv = {"g":(0.001,1)} # here we have a dictionary with a tuple of the conversion factor and the exponent
```

ok now we need to convert kg to grams and compare
```python
to_dict = {"kg":1}

(weight_dict["kg"]/weight_dict["g"])**exponent

to_dict_conv = {"g":(1000,1)}
```

so the conversion factor is then
```python
(from_dict_conv["g"][0]/to_dict_conv["g"][0])

# we compare exponents to validate but do not need them in teh conversion as we have already considered them    
```

## Example 2 explanation and kg m s-2 -> kg m2 s-2 mm-1
```python
from_dict = {"kg":1, "m":1, "s":-2}

from_dict_conv = {"g":(1000,1), "m":(1,1), "s":(1,-2)}

to_dict = {"kg":1, "m":2, "s":-2, "mm":-1}
```
Heres where it gets tricky so we have 3 bins for the conv dictionaries:
- g (mass)
- m (length)
- s (time)

we have mm so that needs to be put into m

```python
# basically we have this (but it cant actually be this because we have 2 identical keys)
to_dict_conv = {"g":(1000,1), "m":(1,2), "s":(1,-2), "m":(.001,-1)}
#combining the m keys (multiply the first digits of the tuple and add the exponents)
to_dict_conv = {"g":(1000,1), "m":(0.001,1), "s":(1,-2)}

multiply the ratios of the first digits
conv_list = [1,1000,1] # this might actally be [1,0.001,1]

#multiplyu elemetns in the list
conv_fact = np.prod(conv_list)


```

so the conversion factor is then



