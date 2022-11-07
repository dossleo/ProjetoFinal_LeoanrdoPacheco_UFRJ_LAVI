from asyncio.format_helpers import extract_stack
from code.time_features_extraction import TimeFeatureExtraction
import dotenv, os

dotenv.load_dotenv()

# if __name__ == '__main__':
#     TimeFeatureExtraction(
#         os.getenv('PATH_2ND_DATABASE')
#     ).execute_time_features()

#     print("Finalizado")

from code.bearing import *

rolamento1 = NewBearing(40,20,10)

rolamento1.freq_gaiola


