import pandas
from tqdm import tqdm
from .models import Tool, ToolUnit, Brand

# Форма для создания экземпляра инструмента
def create_toolunit_from_df(df: pandas.DataFrame):

    for index, row in df.iterrows():
        brand_name = row['brandnames']
        brand, created = Brand.objects.get_or_create(brand_name=brand_name)

        type_tool = row['tool']
        tool, created = Tool.objects.get_or_create(type_tool=type_tool)

        tool_unit = ToolUnit(
            tool=tool,                     
            tool_name=row['tool_name'],            
            brand_name=brand,   
            description = row['descriptions'],
            cover = row['covers'],
        )
        tool_unit.save()