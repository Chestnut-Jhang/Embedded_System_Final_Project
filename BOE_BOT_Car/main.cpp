#include "mbed.h"

//#include "parallax.h"

#include "parallax_servo.h"

#include "bbcar.h"

#include "bbcar_rpc.h"

#include "uLCD_4DGL.h"



DigitalOut led1(LED1);

PwmOut pin12(D12), pin11(D11), pin7(D7), pin6(D6), buzzer(D3);



Serial pc(USBTX, USBRX);



parallax_servo *servo0_ptr, *servo1_ptr, *servo2_ptr, *servo3_ptr;

// parallax_servo servo2(pin7);

// parallax_servo servo3(pin6);

// servo_ticker.attach(&servo_control, .5);

uLCD_4DGL uLCD(D1, D0, D2);

int main() {

    //servo_ticker.attach(&servo_control, .5);

    uLCD.printf("Completeness: 0%%\n");

    bbcar_init(pin11, pin12, pin7, pin6);

    char call, move;

    char buf[256], outbuf[256];

     *servo2_ptr = 0;

     *servo3_ptr = 0;

    wait(5);

    while (1) {

        led1 = 0;

        //wait(1);

        call = pc.getc();

        if (call == 'l'){
        // run the BOE BOT Car on the straight ine

            //*servo2_ptr = 0; *servo3_ptr = 0;  wait(0.5);

            //*servo0_ptr = 0; *servo1_ptr = 0;  wait(0.5);

            for( int i=0; ;i++ ) {

                buf[i] = pc.getc();

                if(buf[i] == '\n') break;

            }

            RPC::call(buf, outbuf);

            pc.printf("%s\r\n", outbuf);

        }

        else if (call == 'm'){
        // run the BOE BOT Car to move the cargo

            //led1 = 1;  wait(1);
            
            ServoStop(0); wait(0.5);

            *servo0_ptr = 30;  *servo1_ptr = 30;  wait(2); // turn right

            //ServoTurn(20, 0.1);  wait(1);

            //ServoCtrl(15);  wait(0.5); // move forward

            ServoStop(0);  wait(0.5);

            pc.putc('D');

            uLCD.printf("Completeness: 20%%\n");

            move = pc.getc();

            if (move == 'y'){

                uLCD.printf("Completeness: 40%%\n");

                ServoCtrl(-30);  wait(2.3); // move backward

                ServoStop(0);  wait(0.5);
                
                *servo0_ptr = 30;  *servo1_ptr = 30;  wait(3.6); // turn around

                *servo0_ptr = 0;  *servo1_ptr = 0;  wait(0.5);

                *servo2_ptr = 0;  *servo3_ptr = 0;  wait(0.5);

                *servo2_ptr = 10;  *servo3_ptr = -10;  wait(2); // control the cargo

                *servo2_ptr = 0;  *servo3_ptr = 0;  wait(0.5);

                uLCD.printf("Completeness: 60%%\n");
                
                ServoCtrl(-30);  wait(3.8); // move backward

                ServoStop(0);  wait(0.5);

                *servo2_ptr = -10;  *servo3_ptr = 10;  wait(2); // control the cargo

                *servo2_ptr = 0;  *servo3_ptr = 0;  wait(0.5);

                uLCD.printf("Completeness: 80%%\n");

                ServoCtrl(15);  wait(3); // move toward

                ServoStop(0);  wait(0.5);

                *servo0_ptr = 40;  wait(2.3); // turn right

                ServoCtrl(15);  wait(2); // move toward

                ServoStop(0);  wait(0.5);

                pc.putc('D');

                uLCD.printf("Completeness: 100%%\n");

            }

            else if (move == 'n'){

                *servo0_ptr = -30;  *servo1_ptr = -30;  wait(2); // turn left

                ServoCtrl(15);  wait(2); // move toward

                ServoStop(0);  wait(0.5);

                pc.putc('D');

            }

        }

    }

}
