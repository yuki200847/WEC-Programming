
# WEC Programming – Energy Distribution Optimization

## Project Overview

Developed as part of the Waterloo Engineering Competition (WEC), this project focuses on optimizing electricity distribution across multiple buildings while accounting for resource limitations, operating costs, and changing environmental conditions.

The system processes inputs from a server, calculates energy allocation and generator production, and outputs electricity distribution results in JSON format.

## How It Works

### 1. Input Processing

The system receives information from a server, including:
- Electricity grid prices
- Random events and equipment availability
- Unit of Energy each building needs

### 2. Energy Allocation and Optimization

The algorithm determines how much electricity each building should receive from available energy sources while respecting system constraints.

It also calculates generator production and accounts for changing operating conditions.

### 3. Output Generation

The system generates electricity allocation results in JSON format, specifying how energy resources are distributed.

## System Constraints

| Constraint | Description |
|---|---|
| Solar generation limit | Maximum solar production of 200 units per hour |
| Building restrictions | The Lecture Hall cannot receive solar electricity |
| Variable grid prices | Electricity prices change over time |
| Generator operating cost | Generator production costs $1 per unit; generator output is used to charge the battery |
| Battery capacity | Battery storage cannot exceed 100 units |
| Weather conditions | Cloudy weather disables solar generation |
| Equipment failures | Grid, battery, or generator equipment may become unavailable |

## Technologies

- **Python** – Energy allocation logic and decisions about how when to charge battery
- **JSON** – Structured electricity allocation output
- **Server-based inputs** – Grid prices, weather forecasts, and random events

## Competition Context

**Waterloo Engineering Competition (WEC)**
