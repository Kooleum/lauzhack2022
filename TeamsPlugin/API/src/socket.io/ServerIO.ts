import * as IO from 'socket.io';
import logger from '../logging/WinstonLogger';
import http from 'http';
import { StatusCodes } from 'http-status-codes';
import { response } from 'express';

// const fetch: Function = require('node-fetch');

class ServerIO extends IO.Server {

    static socket : IO.Socket;
    constructor(server: http.Server) {
        super(server, {
            cors: {
                origin: '*'
            }
        });

        this.on('connection', (socket: IO.Socket) => {
            logger.info(`New connection with ${socket.client.conn.remoteAddress}`);
            
            this.registerEventsOnSocket(socket);
            ServerIO.socket = socket;
        });
    }


    static sendMessage(message: string) {
        console.log("sendMessage");
        // console.log(this.socket);
        this.socket.emit('Message', message);
    }


    private registerEventsOnSocket(socket: IO.Socket) {
        socket.on('Hello', _ => {
            socket.emit('Welcome', socket.id);
        });

    }
}


export default ServerIO;
