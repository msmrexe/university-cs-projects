# Project Overview

As the final project for the Bachelor's course of Computer Networking (4012) at University of Isfahan, students were tasked with implementing the TCP protocol using Python Socket Programming with any number of custom features. These two projcets were therefore personally defined as two variations of the goal.

## Topic

Implementation of TCP Protocol With Custom Features Using Python Socket Programming

Personal Variations:
- Implementation of a Two-Way Chat Betweeem Client and Server + Highspeed Sharing of Any File Format
- Implementation of a Group Chat Betweeem Multiple Clients Via A Shared Server + Highspeed Sharing of Any File Format

## Description

The chat system was implemented using the TCP protocol, incorporating message headers with the username and message type (indicating the presence of an attachment). Clients connect to the server via a predefined port using the IP address specified as input to start messaging. The connection can be terminated with the "over and out" (`/oao`) command.

File transfers are initiated by sending the `ATCHMNT` command along with the local file path, which calls a function that locates, encodes, and packages the file with the appropriate header. Upon receipt, the system automatically identifies the file type, decodes it, and saves it with a unique name based on a file counter. Multiple test runs demonstrated high efficiency in file sharing.
