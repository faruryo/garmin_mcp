"""
Nutrition/food logging functions for Garmin Connect MCP Server
"""
import json

# The garmin_client will be set by the main file
garmin_client = None


def configure(client):
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client


def register_tools(app):
    """Register all nutrition tools with the MCP server app"""

    @app.tool()
    async def get_nutrition_daily_food_log(date: str) -> str:
        """Get daily food consumption records for a date

        Returns food items logged throughout the day including calories,
        macronutrients, and meal associations.

        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            url = f"/nutrition-service/food/logs/{date}"
            data = garmin_client.connectapi(url)
            if not data:
                return f"No food log data found for {date}."
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error retrieving food log data: {str(e)}"

    @app.tool()
    async def get_nutrition_daily_meals(date: str) -> str:
        """Get daily meal summaries for a date

        Returns meal-level summaries (breakfast, lunch, dinner, snacks)
        with nutritional totals for each meal. Each meal includes a mealId
        needed for logging food items to that meal.

        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            url = f"/nutrition-service/meals/{date}"
            data = garmin_client.connectapi(url)
            if not data:
                return f"No meal data found for {date}."
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error retrieving meal data: {str(e)}"

    @app.tool()
    async def get_nutrition_daily_settings(date: str) -> str:
        """Get nutrition plan/settings for a date

        Returns the user's nutrition goals and targets including
        calorie targets, macronutrient goals, and plan configuration.

        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            url = f"/nutrition-service/settings/{date}"
            data = garmin_client.connectapi(url)
            if not data:
                return f"No nutrition settings found for {date}."
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error retrieving nutrition settings: {str(e)}"

    @app.tool()
    async def get_custom_foods(
        search: str = "",
        start: int = 0,
        limit: int = 20,
    ) -> str:
        """Search or list user's custom foods

        Returns custom foods the user has created, with optional search
        filtering. Use this to find foodId and servingId for logging.

        Args:
            search: Optional search expression to filter foods
            start: Starting index for pagination (default 0)
            limit: Maximum number of results (default 20)
        """
        try:
            url = (
                f"/nutrition-service/customFood"
                f"?searchExpression={search}"
                f"&start={start}&limit={limit}"
                f"&includeContent=true"
            )
            data = garmin_client.connectapi(url)
            if not data:
                return "No custom foods found."
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error retrieving custom foods: {str(e)}"

    @app.tool()
    async def get_custom_food_serving_units() -> str:
        """Get available serving units for custom foods

        Returns the list of valid serving units (e.g. G, ML, OZ)
        that can be used when creating custom foods.
        """
        try:
            url = "/nutrition-service/metadata/customFoodServingUnits"
            data = garmin_client.connectapi(url)
            if not data:
                return "No serving units found."
            return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error retrieving serving units: {str(e)}"

    # --- Write tools disabled for read-only mode ---
    # create_custom_food, update_custom_food, log_food have been removed
    # to prevent unintended data modification via prompt injection.

    return app
