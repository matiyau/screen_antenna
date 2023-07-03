#ifndef _RGBLED_H_
#define _RGBLED_H_

#include <Adafruit_MCP3008.h>
#include <PCA9956.h>

class RGBLED {

  public:
    PCA9956 &drv;
    uint8_t drv_ch_r;
    uint8_t drv_ch_g;
    uint8_t drv_ch_b;
  
    uint8_t i_r_val = 0;
    uint8_t i_g_val = 0;
    uint8_t i_b_val = 0;
  
    uint8_t pwm_r_val = 0;
    uint8_t pwm_g_val = 0;
    uint8_t pwm_b_val = 0;
    
    Adafruit_MCP3008 &adc;
    uint8_t adc_ch_r;
  
    RGBLED(PCA9956 &drv, uint8_t drv_ch_r, uint8_t drv_ch_g, uint8_t drv_ch_b, Adafruit_MCP3008 &adc, uint8_t adc_ch_r)
      : drv(drv), drv_ch_r(drv_ch_r), drv_ch_g(drv_ch_g), drv_ch_b(drv_ch_b), adc(adc), adc_ch_r(adc_ch_r) {};
  
    void setPWMR(uint8_t val);
    void setPWMG(uint8_t val);
    void setPWMB(uint8_t val);
    void setPWM(uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setPWM(uint8_t val);
  
    void setIR(uint8_t val);
    void setIG(uint8_t val);
    void setIB(uint8_t val);
    void setI(uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setI(uint8_t val);
  
    int16_t getADCR();
  
};

#endif //_RGBLED_H_
