import console, { Console } from 'console';
import express, { NextFunction } from 'express';
import { StatusCodes } from 'http-status-codes';
import  ServerIO  from '../socket.io/ServerIO';
// path.resolve(--dirname, pathtoDb)

const router: express.Router = express.Router();


router.get('/', (req: express.Request, res: express.Response) => res.status(StatusCodes.OK).end());

router.get('/helloworld', (req: express.Request, res: express.Response) => res.status(StatusCodes.OK).json({ message: 'Hello World' }));


router.post('/message', (req: express.Request, res: express.Response) => {
    let text : string = req.query['text'].toString();
    console.log(text);

    ServerIO.sendMessage(text);

    res.status(StatusCodes.OK).end();
});

router.get('/message', (req: express.Request, res: express.Response) => {


    console.log("text");

    res.status(StatusCodes.OK).end();
});

export default router;
