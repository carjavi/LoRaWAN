function decodeUplink(input) {
    // Crear un nuevo array de bytes que incluya todos los bytes originales
    let extendedBytes = input.bytes.slice(); // Copia los bytes originales

    return { 
        data: Decode(input.fPort, extendedBytes, input.variables)
    };   
}

function Decode(fPort, bytes, variables) {
    // Helper function to convert bytes to an integer in big-endian order
    function bytesToIntBigEndian(bytes) {
        if (bytes.length === 2) {
            return (bytes[0] << 8) | bytes[1]; // Big-endian order: MSB first
        }
        return 0;
    }

    // Extraer el tercer byte (índice 2)
    let tercerByte = bytes[2];

    // Extract bytes from the payload, starting from index 3
    let pay_hex = Array.from(bytes.slice(3), byte => ('0' + byte.toString(16)).slice(-2)).join(', ');

    let distancia = 0;
    let confianza = 0;
    let tercerDato = 0;

    // Verificar si el tercer byte es igual a 01 antes de proceder con la transformación

        // Split pay_hex into parts
        let parts = pay_hex.split(', ').map(hex => parseInt(hex, 16));

        // Check if we have at least 4 parts to accommodate the third data
        if (parts.length >= 3) {
            // Modify the first byte to ignore the first digit
            
            parts[0] = parts[0] & 0x0F;
            // Use big-endian order for the distance (first two bytes)
            let distanceBytes = [parts[0], parts[1]]; 
            distancia = bytesToIntBigEndian(distanceBytes);

            parts[2] = parts[2] & 0x0F;

          // Extract the confidence (third byte in pay_hex)
          let confianzaBytes = [parts[2], parts[3]]; // Keep order as '80 64'
          confianza = bytesToIntBigEndian(confianzaBytes);

        
        }

        // Convert distance to meters if needed
        distancia = distancia;


    return { 
        distancia: distancia, // Solo se convierte si tercerByte es 01
        confianza: confianza,
        //pay_hex: pay_hex
    }
}