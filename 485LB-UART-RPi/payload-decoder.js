function decodeUplink(input) {
    // Crear un nuevo array de bytes que incluya todos los bytes originales
    let extendedBytes = input.bytes.slice(); // Copia los bytes originales

    return { 
        data: Decode(input.fPort, extendedBytes, input.variables)
    };   
}

function Decode(fPort, bytes, variables) {

    // Convierte el payload en valores numéricos.
    let BatV = ((bytes[0]<<8 | bytes[1])&0x7fff)/1000;
    let Registro1 = ((bytes[3]<<8 | bytes[4])&0x7fff);
    let Registro2 = ((bytes[5]<<8 | bytes[6])&0x7fff);
    let Registro3 = ((bytes[7]<<8 | bytes[8])&0x7fff);
    let Registro4 = ((bytes[9]<<8 | bytes[10])&0x7fff);


    return { 
        BatV: BatV,
        Registro1: Registro1, // Solo se convierte si tercerByte es 01
        Registro2: Registro2,
        Registro3: Registro3,
        Registro4: Registro4
    }
}