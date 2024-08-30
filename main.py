import nextcord
from nextcord.ext import commands
import os
import math
import random
import asyncio

# Set up the bot
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

# Dictionary of available operations and their descriptions
OPERATIONS = {
    'abs': 'Absolute value',
    'round': 'Round to the nearest integer',
    'min': 'Minimum value',
    'max': 'Maximum value',
    'pow': 'Power (x^y)',
    'sqrt': 'Square root',
    'sin': 'Sine (in radians)',
    'cos': 'Cosine (in radians)',
    'tan': 'Tangent (in radians)',
    'pi': 'Mathematical constant pi',
    'e': 'Mathematical constant e'
}

# Dictionary for unit conversions
UNIT_CONVERSIONS = {
    'km_to_miles': lambda x: x * 0.621371,
    'miles_to_km': lambda x: x * 1.60934,
    'kg_to_lbs': lambda x: x * 2.20462,
    'lbs_to_kg': lambda x: x * 0.453592,
    'celsius_to_fahrenheit': lambda x: x * 9/5 + 32,
    'fahrenheit_to_celsius': lambda x: (x - 32) * 5/9
}

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.slash_command(name="help", description="Get help on how to use the calculator bot")
async def help(interaction: nextcord.Interaction):
    help_message = (
        "Welcome to the Calculator Bot!\n\n"
        "Available commands:\n"
        "/calculate: Perform calculations\n"
        "/convert: Convert units\n"
        "/mathproblem: Get a math problem to solve\n\n"
        "Available operations and constants for /calculate:\n"
    )
    
    for op, desc in OPERATIONS.items():
        help_message += f"• `{op}`: {desc}\n"
    
    help_message += (
        "\nExamples of complex calculations:\n"
        "• `/calculate equation:sin(pi/4) + cos(pi/3)`\n"
        "• `/calculate equation:max(10, 5, 8) * min(3, 6, 2)`\n"
        "• `/calculate equation:sqrt(pow(3, 2) + pow(4, 2))`\n\n"
        "Unit conversion: `/convert value:<value> from_unit:<unit> to_unit:<unit>`\n"
        "Example: `/convert value:10 from_unit:km to_unit:miles`\n\n"
        "Start a math problem: `/mathproblem`\n\n"
        "Note: All trigonometric functions use radians, not degrees."
    )
    
    await interaction.response.send_message(help_message)

@bot.slash_command(name="calculate", description="Perform a calculation")
async def calculate(interaction: nextcord.Interaction, equation: str):
    try:
        # Create a dictionary with safe mathematical functions
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'pow': pow,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        }

        # Evaluate the equation using the safe dictionary
        result = eval(equation, {"__builtins__": None}, safe_dict)
        
        await interaction.response.send_message(f"The result of `{equation}` is: {result}")
    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}")

@bot.slash_command(name="convert", description="Convert units")
async def convert(interaction: nextcord.Interaction, value: float, from_unit: str, to_unit: str):
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in UNIT_CONVERSIONS:
        result = UNIT_CONVERSIONS[conversion_key](value)
        await interaction.response.send_message(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")
    else:
        await interaction.response.send_message(f"Conversion from {from_unit} to {to_unit} is not supported.")

@bot.slash_command(name="mathproblem", description="Get a math problem to solve")
async def mathproblem(interaction: nextcord.Interaction):
    problem_types = [
        "addition",
        "subtraction",
        "multiplication",
        "division",
        "exponentiation",
        "square_root",
        "percentage"
    ]
    problem_type = random.choice(problem_types)

    if problem_type == "addition":
        a, b = random.randint(1, 100), random.randint(1, 100)
        problem = f"{a} + {b}"
        correct_answer = a + b
    elif problem_type == "subtraction":
        a, b = random.randint(1, 100), random.randint(1, 100)
        problem = f"{max(a, b)} - {min(a, b)}"
        correct_answer = abs(a - b)
    elif problem_type == "multiplication":
        a, b = random.randint(1, 12), random.randint(1, 12)
        problem = f"{a} × {b}"
        correct_answer = a * b
    elif problem_type == "division":
        b = random.randint(1, 12)
        a = b * random.randint(1, 12)
        problem = f"{a} ÷ {b}"
        correct_answer = a / b
    elif problem_type == "exponentiation":
        a = random.randint(2, 5)
        b = random.randint(2, 3)
        problem = f"{a}^{b}"
        correct_answer = a ** b
    elif problem_type == "square_root":
        a = random.randint(1, 10)
        problem = f"√{a**2}"
        correct_answer = a
    elif problem_type == "percentage":
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        problem = f"{a}% of {b}"
        correct_answer = (a / 100) * b

    await interaction.response.send_message(f"Solve this math problem: {problem}")

    def check(m):
        return m.channel == interaction.channel

    end_time = asyncio.get_event_loop().time() + 60.0  # 60 seconds time limit

    while True:
        try:
            remaining_time = end_time - asyncio.get_event_loop().time()
            if remaining_time <= 0:
                await interaction.followup.send("Time's up! No one answered correctly.")
                return

            msg = await bot.wait_for('message', check=check, timeout=remaining_time)
            
            try:
                user_answer = float(msg.content)
                if abs(user_answer - correct_answer) < 0.01:  # Allow for small floating-point errors
                    await interaction.followup.send(f"The winner is {msg.author.mention}!")
                    return
                else:
                    await interaction.followup.send(f"Wrong answer, {msg.author.mention}. Try again!")
            except ValueError:
                await interaction.followup.send(f"Invalid input, {msg.author.mention}. Please enter a number.")
        
        except asyncio.TimeoutError:
            await interaction.followup.send("Time's up! No one answered correctly.")
            return

bot.run('MTI2Njg0NDI5NzE3MzQwNTg1MA.G0uSNE.GEcVyoOaC3P17EFLdMkkSXeF4YZF_v-J2Gl1y4')