# UDS over CAN


We have discussed CAN-TP, and now let us look at a practical example using real CAN traces captured from a vehicle.

A typical CAN trace includes a timestamp, an indication of whether the frame is transmitted or received, the CAN identifier, the DLC (Data Length Code), and the data payload. In classical CAN, the payload consists of up to 8 bytes, labeled from D0 to D7.

For illustration, we focus on a small subset of frames related to CAN Transport Protocol. These frames together represent a segmented data transfer.

In the first frame, the DLC is 8 and the data bytes are indexed from D0 to D7. The payload begins with the byte sequence:

10 12 36 01 01 31 47 31

The first byte, 0x10, indicates a First Frame in CAN-TP. The next byte, 0x12, represents the total payload length. In hexadecimal, 0x12 corresponds to 18 bytes of application data. This means the message cannot fit into a single CAN frame and must be segmented.

The byte 0x36 represents the UDS service identifier for Transfer Data. The subsequent bytes include the block sequence counter and the initial portion of the payload.

The next frame in the trace is:

30 00 00 00 00 00 00 00

This frame is sent by the receiver and represents a Flow Control frame. The first nibble 0x3 indicates Flow Control. The flow status value 0x00 means Continue To Send. The remaining bytes specify block size and separation time. In this case, both are zero, indicating that the sender may continue transmitting without delay and without block size restriction.

Following the Flow Control frame, the sender transmits Consecutive Frames. These frames start with identifiers such as 0x21, 0x22, and so on. The high nibble 0x2 indicates a Consecutive Frame, while the low nibble represents the sequence number. Each consecutive frame carries up to 7 bytes of payload in standard addressing.

As the transfer progresses, the sequence numbers increment, allowing the receiver to reassemble the complete message in the correct order. If the configured block size is reached, the sender pauses and waits for another Flow Control frame before continuing.

The timing between consecutive frames is governed by the separation time parameter defined in the Flow Control frame. This ensures that the receiver is not overwhelmed and that communication remains reliable.

In summary, this trace demonstrates the complete CAN-TP flow: a First Frame announcing a multi-frame message, a Flow Control response from the receiver, followed by a series of Consecutive Frames carrying the remaining data. This mechanism enables reliable transmission of diagnostic and flashing data well beyond the 8-byte CAN frame limitation.

This example illustrates how CAN-TP operates in real vehicle communication and how large diagnostic payloads are safely transferred over CAN.
