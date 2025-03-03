import tkinter as tk
import re


def convert_units(value, unit):
    # Define the unit multipliers for different units
    unit_multipliers = {
        "million": 1e6, "billion": 1e9,
        "hz": 1, "khz": 1e3, "mhz": 1e6, "ghz": 1e9,
        "s": 1, "ms": 1e-3, "us": 1e-6, "ns": 1e-9
    }
    unit = unit.lower()
    return value * unit_multipliers.get(unit, 1)

def format_units(value, unit):
    # Define the units and their prefixes
    units = [
        (1e9, 'G'),
        (1e6, 'M'),
        (1e3, 'k'),
        (1, ''),
        (1e-3, 'm'),
        (1e-6, 'µ'),
        (1e-9, 'n')
    ]
    # Define the numerical term associated with each prefix
    replacement_units = {
        'G': 'billion',
        'M': 'million',
        'k': 'thousand',
        'm': 'milli',
        'µ': 'micro',
        'n': 'nano'
    }

    for factor, prefix in units:
        if value >= factor:
            if unit == "":
                return f"{value / factor:.2f} {replacement_units[prefix]}{unit}"
            else:
                return f"{value / factor:.2f} {prefix}{unit}"

def extract_values(text):
    keywords = {
        "clock cycle time": "clock_cycle_time",
        "clock cycles": "clock_cycles",
        "clock rate": "clock_rate",
        "cpi": "cpi",
        "instruction count": "instruction_count"
    }

    values = {}
    # Extract values and units
    for keyword, key in keywords.items():
        pattern = rf"{keyword}.*?(\d+\.?\d*)\s*([a-zA-Z]*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            unit = match.group(2)  # Extract unit
            values[key] = convert_units(value, unit)

    return values


def solve_problem():
    problem_text = text_box.get("1.0", tk.END).strip()
    result_label.config(text="Processing...")

    values = extract_values(problem_text)
    result = ""

    # Compute the clock rate, clock cycles, and execution time
    if "clock_cycle_time" in values:
        values["clock_rate"] = 1 / values["clock_cycle_time"]
        result += f"Clock Rate = 1 / clock cycle time = {format_units(1/values['clock_cycle_time'], 'Hz')}\n"
    if "cpi" in values and "instruction_count" in values:
        values["clock_cycles"] = values["cpi"] * values["instruction_count"]
        result += f"Clock Cycles = cpi * instruction count = {format_units(values['cpi'] * values['instruction_count'], '')}\n"
    if "clock_cycles" in values and "clock_rate" in values:
        result += f"Execution Time = clock cycles / clock rate = {format_units(values['clock_cycles'] / values['clock_rate'], 's')}\n"
    else:
        result = "Could not compute execution time. Please provide more details."

    result_label.config(text=result)


# Create the main window
root = tk.Tk()
root.title("Flexible Math Word Problem Solver")

# Create a text box
text_box = tk.Text(root, height=5, width=50)
text_box.pack()

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=solve_problem)
submit_button.pack()

# Create a label for the result
result_label = tk.Label(root, text="Enter a problem and press Submit.")
result_label.pack()

# Run the application
root.mainloop()

# Test input
# A processor has a clock cycle time of 2.5 ns and clock cycles of 10 million.
# A processor has a clock rate of 2.5 billion, CPI of 1.5, and instruction count of 10 million.