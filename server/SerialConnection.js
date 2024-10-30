const { SerialPort } = require('serialport');
const prompt = require("prompt-sync")({ sigint: true });

// PONER PUERTO SERIAL CORRECTO
const port = new SerialPort({ path: 'COM4', baudRate: 9600 });

let inProcess = true;

let startMovement = () => {
    port.write('empezarrecorrido', function(err) {
        if (err) {
            return console.log('Error on write: ', err.message);
        }
        console.log('Mensaje enviado: empezarrecorrido');
    });
};

// Manejo de errores del puerto
port.on('error', function(err) {
    console.log('Error de puerto serial: ', err.message);
});

// Leer los datos que vienen del puerto serial (opcional, si el Arduino envía datos)
let readData = () =>{
  port.on('data', function(data) {
      return data.toString();
  });
}


