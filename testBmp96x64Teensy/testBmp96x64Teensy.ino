//Test code to read bmp file over a 16 bit coded array
//By Enzo Niro - protongamer

#include <SPI.h>
#include <SSD_13XX.h>
#include "bmp_data.h" // bitmap arrays

// For the Adafruit shield, these are the default.
#define TFT_DC  9
#define TFT_CS 10
#define TFT_RS 8

uint8_t errorCode = 0;

SSD_13XX tft = SSD_13XX(TFT_CS, TFT_DC, TFT_RS);

//Prototype function
void drawBmp(uint8_t _x, uint8_t _y, const uint16_t bmp[64][96]);

void setup() {
Serial.begin(115200);

  tft.begin(false);

  //the following it's mainly for Teensy
  //it will help you to understand if you have choosed the
  //wrong combination of pins!
  errorCode = tft.getErrorCode();
  if (errorCode != 0) {
    Serial.print("Init error! ");
    if (bitRead(errorCode, 0)) Serial.print("MOSI or SCLK pin mismach!\n");
    if (bitRead(errorCode, 1)) Serial.print("CS or DC pin mismach!\n");
  }


  drawBmp(0,0,logo); //Read and display logo array at coordinate XY(0,0)

}


void drawBmp(uint8_t _x, uint8_t _y, const uint16_t bmp[64][96]){//function to read bitmap array

for(byte j = 63; j > 0; j--){
 for(byte i = 0; i < 128; i++){

  //the first line in array is the last of the bmp
  //first word is located on left down of the bmp
  tft.drawPixel(_x+i,_y+j,pgm_read_word(&bmp[63-j][i]));
 }
}


}






void loop(void) {
//Do your personal code here :)
}


