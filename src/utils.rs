
use std::{net::UdpSocket, env, process::Command, os::windows::process::CommandExt, io::{BufReader, BufRead, Read}};

use crypto::{md5::Md5, digest::Digest, rc4::Rc4, symmetriccipher::SynchronousStreamCipher};
use nwg::{MessageParams, MessageButtons, MessageIcons, MessageChoice};
use base64::{encode, decode};

use winapi::{um::winuser, shared::windef::HWND};

pub fn dialog_info(text: &str) {
    let params = MessageParams {
        title: "Info",
        content: text,
        buttons: MessageButtons::Ok,
        icons: MessageIcons::Info
    };
    let hwnd = unsafe { winuser::GetDesktopWindow() };
    inner_message(hwnd, &params);
}

pub fn dialog_error(text: &str) {
    let params = MessageParams {
        title: "Info",
        content: text,
        buttons: MessageButtons::Ok,
        icons: MessageIcons::Error
    };
    let hwnd = unsafe { winuser::GetDesktopWindow() };
    inner_message(hwnd, &params);
}

pub fn dialog(text: &str) {
    let params = MessageParams {
        title: "Info",
        content: text,
        buttons: MessageButtons::Ok,
        icons: MessageIcons::None
    };
    let hwnd = unsafe { winuser::GetDesktopWindow() };
    inner_message(hwnd, &params);
}

fn to_utf16<'a>(s: &'a str) -> Vec<u16> {
    use std::ffi::OsStr;
    use std::os::windows::ffi::OsStrExt;

    OsStr::new(s)
      .encode_wide()
      .chain(Some(0u16).into_iter())
      .collect()
}

fn inner_message(parent: HWND, params: &MessageParams) -> MessageChoice {
    use winapi::um::winuser::{MB_ABORTRETRYIGNORE, MB_CANCELTRYCONTINUE, MB_OK, MB_OKCANCEL, MB_RETRYCANCEL, MB_YESNO,
        MB_YESNOCANCEL, MB_ICONSTOP, MB_ICONINFORMATION, MB_ICONQUESTION, MB_ICONEXCLAMATION};
   
       use winapi::um::winuser::{IDABORT, IDCANCEL, IDCONTINUE, IDIGNORE, IDNO, IDOK, IDRETRY, IDTRYAGAIN, IDYES};
       use winapi::um::winuser::MessageBoxW;
   
       let text = to_utf16(params.content);
       let title = to_utf16(params.title);
   
       let buttons = match params.buttons {
           MessageButtons::AbortTryIgnore => MB_ABORTRETRYIGNORE,
           MessageButtons::CancelTryContinue => MB_CANCELTRYCONTINUE,
           MessageButtons::Ok => MB_OK,
           MessageButtons::OkCancel => MB_OKCANCEL,
           MessageButtons::RetryCancel => MB_RETRYCANCEL,
           MessageButtons::YesNo => MB_YESNO,
           MessageButtons::YesNoCancel => MB_YESNOCANCEL
       };
   
       let icons = match params.icons {
           MessageIcons::Error => MB_ICONSTOP,
           MessageIcons::Info => MB_ICONINFORMATION,
           MessageIcons::None => 0,
           MessageIcons::Question => MB_ICONQUESTION,
           MessageIcons::Warning => MB_ICONEXCLAMATION
       };
   
       let answer = unsafe{ MessageBoxW(parent, text.as_ptr(), title.as_ptr(), buttons | icons) };
       match answer {
           IDABORT => MessageChoice::Abort,
           IDCANCEL => MessageChoice::Cancel,
           IDCONTINUE => MessageChoice::Continue,
           IDIGNORE => MessageChoice::Ignore,
           IDNO => MessageChoice::No,
           IDOK => MessageChoice::Ok,
           IDRETRY => MessageChoice::Retry,
           IDTRYAGAIN => MessageChoice::TryAgain,
           IDYES => MessageChoice::Yes,
           _ => MessageChoice::Cancel
       }
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
    println!("{} {}", result[1].replace("\n", "").replace(" ", ""), result.len());
    let cpu_id = result[1].replace("\n", "").replace(" ", "");
    let mut hwid = format!("{}-{}", "TH3RA1NB0W", cpu_id);
    let mut md5_build = Md5::new();
    md5_build.input_str(&hwid);
    hwid = md5_build.result_str();
    return hwid;
}

pub fn rc4_encode(text: String, key: String) -> String {
    let text_bytes = text.as_bytes();
    let k = format!("{}", key);
    let mut rc4 = Rc4::new(key.as_bytes());
    let mut ciphertext = vec![0; text_bytes.len()];
    rc4.process(text_bytes, &mut ciphertext);

    encode(&ciphertext)
}

pub fn rc4_decode(text: String, key: String) -> String {
    let dec_text = decode(text).unwrap();
    //println!("{}", String::from_utf8(dec_text.clone()).unwrap());
    let mut rc4 = Rc4::new(key.as_bytes());
    let mut plaintext = vec![0; dec_text.len()];
    rc4.process(&dec_text, &mut plaintext);

    match String::from_utf8(plaintext) {
        Ok(o) => return o,
        Err(_) => {
            dialog_error("decode ERROR!");
            return String::new();
        },
    }
}