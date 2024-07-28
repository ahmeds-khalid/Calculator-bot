import nextcord
from nextcord.ext import commands
import os
import math

# Set up the bot
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

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

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

@bot.slash_command(name="help", description="Get help on how to use the calculator bot")
async def help(interaction: nextcord.Interaction):
    help_message = (
        "Welcome to the Calculator Bot!\n\n"
        "To use the calculator, type `!calc` followed by your equation. For example:\n"
        "`!calc 2 + 2`\n"
        "`!calc sqrt(16) + pow(2, 3)`\n\n"
        "Available operations and constants:\n"
    )

    for op, desc in OPERATIONS.items():
        help_message += f"• `{op}`: {desc}\n"

    help_message += (
        "\nExamples of complex calculations:\n"
        "• `!calc sin(pi/4) + cos(pi/3)`\n"
        "• `!calc max(10, 5, 8) * min(3, 6, 2)`\n"
        "• `!calc sqrt(pow(3, 2) + pow(4, 2))`\n\n"
        "Note: All trigonometric functions use radians, not degrees."
    )

    await interaction.response.send_message(help_message)

@bot.command(name='calc')
async def calc(ctx, *, equation: str):
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

        await ctx.send(f"The result of `{equation}` is: {result}")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

bot.run("MTI2Njg0NDI5NzE3MzQwNTg1MA.Gk1miF.KeqW5q77nawnekTciLkNqml_WDJLX-DywQaAww")
