const { SerialPort } = require('serialport');
const prompt = require("prompt-sync")({ sigint: true });
const express =  require('express');
const app = express();
const bodyparser = require("body-parser");
const morgan = require("morgan");
const fs = require("fs");
const { STATUS_CODES } = require('http');
const PORT = process.env.PORT || 3466;
//-----------------
// Importa la API de Google y configura el módulo Google Sheets
const { google } = require("googleapis");
const sheets = google.sheets("v4"); // Inicializa el servicio de Google Sheets
require("dotenv").config(); // Carga las variables de entorno desde el archivo .env
//----------------

const port = new SerialPort({ path: 'COM4', baudRate: 9600 });
app.set('view engine', 'pug');
app.set('views', './views');
app.use(express.static('public'));
app.use(express.static('css'));
app.use(morgan("tiny"));
app.use(express.json({limit : '30MB'}));
app.use(express.urlencoded({ extended: true }));

//------------
// Función para obtener datos de Google Sheets
async function getSheetData() {
    // Configura la autenticación con las credenciales de Google en el archivo JSON
    const auth = new google.auth.GoogleAuth({
      keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS, // Ruta a las credenciales
      scopes: ["https://www.googleapis.com/auth/spreadsheets.readonly"], // Define los permisos de solo lectura
    });
  
    const client = await auth.getClient(); // Obtiene el cliente de autenticación
    const spreadsheetId = "1hNjs7kg0sZ5EWgegud1xc74MwTGk2to3UW21tfiWI7w"; // ID de la hoja de cálculo
    const range = "Hoja 1"; // Nombre de la hoja completa para obtener todos los valores
  
    // Realiza la solicitud para obtener los valores de la hoja especificada
    const response = await sheets.spreadsheets.values.get({
      auth: client,
      spreadsheetId: spreadsheetId,
      range: range, // Obtiene todos los datos de la hoja especificada
    });
  
    return response.data.values; // Retorna los valores obtenidos
  }
  

  
  // Ruta para obtener los datos de Google Sheets
  app.get("/sheetdata", async (req, res) => {
    try {
      const rows = await getSheetData(); // Espera la resolución de getSheetData
      if (rows && rows.length > 0) {
        const lastRow = rows[rows.length - 1]; // Obtener la última fila con datos
        res.render('indexpug', {lastRow}); // Enviar la última fila como respuesta en JSON
      } else {
        res.status(404).send("No data found.");
      }
    } catch (error) {
      console.error("Error al obtener datos de Google Sheets:", error.message, error.response?.data);
      res.status(500).send("Error al obtener datos");
    }
  });
  //------------

app.get('/', (req, res) => {
    res.render('indexpug')
})

app.post('/newupload', (req, res) => {
    let image64 = req.body ["uploadedimage"];
    let buffer = Buffer.from(image64, "base64");
    fs.writeFileSync("public/imagendescargada.png", buffer);

})

app.post('/auth', (req, res) => {
    let msg1 = req.body.key1
    let msg2 = req.body.key2
    console.log(msg1+' '+msg2)
    res.send(200)

})

app.get('/shoot', (req, res) =>{
    //Lamamos el serialConnection.
    startMovement()
    console.log(readData())
    console.log('shooting...')
    res.render('indexpugimg')

})

app.listen(PORT, () =>{
    console.log('LISTENING TO PORT 3466');
    console.log('ENDPOINTS: \n/\n/uploadimage');
});


// PONER PUERTO SERIAL CORRECTO

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

app.get("/sheetdata1", async (req, res) => {
  try {
    const rows = await getSheetData(); // Espera la resolución de getSheetData
    if (rows && rows.length > 0) {
      res.render('records', {rows}); 
    } else {
      res.status(404).send("No data found.");
    }
  } catch (error) {
    console.error("Error al obtener datos de Google Sheets:", error.message, error.response?.data);
    res.status(500).send("Error al obtener datos");
  }
});


