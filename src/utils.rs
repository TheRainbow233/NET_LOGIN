
use std::{net::UdpSocket, process::Command, os::windows::process::CommandExt, io::{BufReader, BufRead}, path::PathBuf};

use crypto::{md5::Md5, digest::Digest, rc4::Rc4, symmetriccipher::SynchronousStreamCipher};
use base64::{encode, decode};

pub fn get_exepath() -> PathBuf {
    std::env::current_exe().unwrap()
}

pub fn get_path() -> PathBuf {
    std::env::current_dir().unwrap()
}

pub fn get_ip() -> Option<String> {
    let socket = match UdpSocket::bind("0.0.0.0:0") {
        Ok(s) => s,
        Err(_) => return None,
    };
 
    match socket.connect("8.8.8.8:80") {
        Ok(()) => (),
        Err(_) => return None,
    };
 
    match socket.local_addr() {
        Ok(addr) => return Some(addr.ip().to_string()),
        Err(_) => return None,
    };
}

pub fn get_hwid() -> String {
    let text = "wmic cpu get ProcessorId";
    let cmd = Command::new("cmd").creation_flags(0x08000000).arg("/c").arg(text).output().expect("cmd exec error!");
    let result = BufReader::new(&cmd.stdout[..])
                           .lines()
                           .map(|l| l.expect("Could not parse line"))
                           .collect::<Vec<String>>();
    //println!("{} {}", result[1].replace("\n", "").replace(" ", ""), result.len());
    let cpu_id = result[1].replace("\n", "").replace(" ", "");
    let mut hwid = format!("{}-{}", "TH3RA1NB0W", cpu_id);
    let mut md5_build = Md5::new();
    md5_build.input_str(&hwid);
    hwid = md5_build.result_str();
    return hwid;
}

pub fn rc4_encode(text: String, key: String) -> String {
    let text_bytes = text.as_bytes();
    let mut rc4 = Rc4::new(key.as_bytes());
    let mut ciphertext = vec![0; text_bytes.len()];
    rc4.process(text_bytes, &mut ciphertext);

    encode(&ciphertext)
}

pub fn rc4_decode(text: String, key: String) -> String {
    let dec_text = decode(text).unwrap();
    let mut rc4 = Rc4::new(key.as_bytes());
    let mut plaintext = vec![0; dec_text.len()];
    rc4.process(&dec_text, &mut plaintext);

    match String::from_utf8(plaintext) {
        Ok(o) => return o,
        Err(_) => {
            nwg::error_message("Error", "Config_Decode ERROR!");
            return String::new();
        },
    }
}