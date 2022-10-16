# Halloween Doorbell

This is a personal project I worked on for Halloween 2022. The purpose of this project was to create a doorbell from a cheap Target halloween doorbell prop (see below).

## Parts
1. Raspberry Pi
2. Spare cables (I used cables from other halloween props and speaker wire I had left over)
3. Home assistant
4. [A halloween doorbell prop](https://www.target.com/p/animated-doorbell-with-eye-halloween-decorative-prop-hyde-38-eek-boutique-8482/-/A-83940532#lnk=sametab)

### Process
I first had to figure out how to get input from the binary buton on the haloween prop to the raspberry pi. For me, who has hardly dabbled in electronics at all, this was the hardest part. I used a multimeter to check the voltage of the button pins inside the prop and found that the are always high until the button is pressed. When the button is pressed, the voltage is driven low until the button is released. However, the props will begin playing sound and moving on the leading edge, so I just had to listen for that.

Once I was able to figure out how to get an input, I wired some spare cables to the button pins. Once connected, I was able to pin these cables into the raspberry pi. At which point, I was able to start programming. After a couple of debugging sessions, I was able to set up the following flow:

![code flow](./code-flow.png)

At which point, I needed to now set up a method in which for the raspberry pi to communicate with home assistant. Since I already had home assistant running, i just needed the MQTT integration set up. There are many guides for this step online. Once I had the integration set up, I tested it to ensure that pressing the button multiple times won't messed up the state (since I opted to not try to grab state by checking the volage in the prop).

The final result is a doorbell which will notify my wife and I on our phones and TV without ringing the actual doorbell and a fun experience for kids to have when trick-or-treating. In combination with with a tube to act as a candy shute, we also not don't have to walk up and down stairs to pass out candy (first world problem, I know..)
