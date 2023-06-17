#![windows_subsystem = "windows"]

mod utils;

extern crate native_windows_derive as nwd;
extern crate native_windows_gui as nwg;

use std::{
    env,
    fs::{self, File},
    io,
    path::{Path, PathBuf},
};

use nwd::NwgUi;
use nwg::{CheckBoxState, NativeUi};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use winreg::{enums::HKEY_CURRENT_USER, RegKey};

#[derive(Serialize, Deserialize, Debug)]
struct Config {
    account: String,
    password: String,
    operators: String,
    autostart: bool,
}

#[derive(Default, NwgUi)]
pub struct GuiBuilder {
    #[nwg_control(size: (370, 160), position: (300, 300), title: "NET_LOGIN", flags: "WINDOW|VISIBLE", center: true)]
    #[nwg_events( OnWindowClose: [GuiBuilder::stop] )]
    window: nwg::Window,

    #[nwg_layout(parent: window, spacing: 1)]
    grid: nwg::GridLayout,

    #[nwg_resource(family: "Microsoft Yahei", size: 18)]
    font: nwg::Font,

    #[nwg_control(text: "Account", size: (80, 20), position: (20, 9), font: Some(&data.font))]
    label1: nwg::Label,
    #[nwg_control(text: "", focus: true, size: (150, 22), position: (80, 7), font: Some(&data.font))]
    //#[nwg_layout_item(layout: grid, row: 0, col: 0)]
    account_edit: nwg::TextInput,

    #[nwg_control(text: "Password", size: (80, 20), position: (12, 44), font: Some(&data.font))]
    label2: nwg::Label,
    #[nwg_control(text: "", focus: true, size: (150, 22), position: (80, 40), password: Some('*'), font: Some(&data.font))]
    //#[nwg_layout_item(layout: grid, row: 0, col: 0)]
    password_edit: nwg::TextInput,

    #[nwg_control(collection: vec!["ChinaMobile", "ChinaTelecom", "ChinaUnicom"], selected_index :Some(0), size: (120, 4), position: (240, 6), font: Some(&data.font))]
    combo_box: nwg::ComboBox<&'static str>,

    #[nwg_control(text: "AutoStart", position: (80, 68), font: Some(&data.font))]
    #[nwg_events( OnButtonClick: [GuiBuilder::auto_start] )]
    auto_start: nwg::CheckBox,

    #[nwg_control(text: "Login", size: (110, 50), position: (130, 99), font: Some(&data.font))]
    #[nwg_events( OnButtonClick: [GuiBuilder::login_click] )]
    login_button: nwg::Button,
}

impl GuiBuilder {
    fn stop(&self) {
        nwg::stop_thread_dispatch()
    }

    fn dialog_info(&self, text: &str) {
        nwg::modal_info_message(&self.window, "Info", &format!("{}", text));
    }

    fn auto_start(&self) {
        let b = self.auto_start.check_state();
        let key_name = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
        let hklm = RegKey::predef(HKEY_CURRENT_USER);
        match b {
            CheckBoxState::Checked => {
                let get_key = hklm.create_subkey(key_name);
                match get_key {
                    Ok((reg, _)) => {
                        let exe_path = format!("\"{}\" -a", get_exepath().to_str().unwrap());
                        reg.set_value("NET_LOGIN", &exe_path).unwrap();
                        let reg_text: String =
                            reg.get_value("NET_LOGIN").expect("readRegister ERROR!");
                        self.dialog_info(&reg_text);
                    }
                    Err(err) => utils::dialog_error(&err.to_string()),
                }
            }
            CheckBoxState::Unchecked => {
                let get_key = hklm.create_subkey(key_name);
                match get_key {
                    Ok((reg, _)) => {
                        reg.delete_value("NET_LOGIN").unwrap();
                    }
                    Err(_) => {}
                }
            }
            CheckBoxState::Indeterminate => {}
        }
    }

    fn login_click(&self) {
        let account = self.account_edit.text();
        let password = self.password_edit.text();
        let combo = self.combo_box.selection_string().unwrap();
        println!("{}", combo);
        if account != "" && password != "" {
            let operators: &str = match &combo as &str {
                "ChinaMobile" => "cmcc",
                "ChinaTelecom" => "telecom",
                "ChinaUnicom" => "unicom",
                &_ => todo!(),
            };
            let login = login(account, password, operators.to_string());
            match login {
                Some(mut config) => {
                    let check_box = self.auto_start.check_state();
                    let auto_start = match check_box {
                        CheckBoxState::Checked => true,
                        CheckBoxState::Unchecked => false,
                        CheckBoxState::Indeterminate => false,
                    };
                    config.autostart = auto_start;
                    save_config(config);
                },
                None => todo!(),
            }
        }
    }
}

fn get_exepath() -> PathBuf {
    std::env::current_exe().unwrap()
}

fn get_path() -> PathBuf {
    std::env::current_dir().unwrap()
}

fn save_config(config: Config) {
    let path = get_path().join("NL_config");
    let npath = Path::new(&path);
    if !Path::new(&path).exists() {
        File::create(npath).unwrap();
    }
    let mut json = serde_json::to_string(&config).unwrap();
    json = utils::rc4_encode(json, utils::get_hwid());
    fs::write(npath, json).unwrap();
}

fn load_config() -> Option<Config> {
    let path = get_path().join("NL_config");
    let npath = Path::new(&path);
    if !Path::new(&path).exists() {
        File::create(npath).unwrap();
        return None;
    }
    match fs::read_to_string(npath) {
        Ok(str) => {
            let raw = utils::rc4_decode(str, utils::get_hwid());
            match serde_json::from_str(&raw) as Result<Config, serde_json::Error> {
                Ok(config) => {
                    return Some(config);
                }
                Err(_) => {}
            }
        }
        Err(_) => {}
    }
    utils::dialog_error("Config_Load ERROR!");
    None
}

fn login(account: String, password: String, operators: String) -> Option<Config> {
    let url = format!("http://192.168.40.2:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=,0,{}@{}&user_password={}&wlan_user_ip={}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.2&terminal_type=1&lang=zh-cn&v=4836&lang=zh", account, operators, password, utils::get_ip().unwrap());
    println!("{}", url);
    let get = minreq::get(url).send();
    match get {
        Ok(res) => {
            let retu_str = res.as_str().unwrap();
            if !retu_str.contains("dr1003") {
                utils::dialog_error(&format!("Login Error!:\n{}", retu_str));
            }
            let mut retu_msg = retu_str
                .trim_start_matches("dr1003(")
                .trim_end_matches(");");
            let serde: Value = serde_json::from_str(retu_msg).unwrap();
            retu_msg = serde.get("msg").unwrap().as_str().unwrap();
            println!("{}", retu_str);
            utils::dialog(retu_msg);
            return Some(Config {
                account: account,
                password: password,
                operators: operators,
                autostart: false,
            });
        }
        Err(err) => {
            utils::dialog_error(err.to_string().as_str());
        }
    }
    None
}

fn main() {
    let mut config = Config {
        account: String::new(),
        password: String::new(),
        operators: String::new(),
        autostart: false,
    };

    match load_config() {
        Some(cfg) => {
            config = cfg;
        }
        None => {}
    }

    let args: Vec<String> = env::args().collect();
    for i in args {
        if i.contains("-a") {
            login(config.account, config.password, config.operators).unwrap();
            std::process::exit(0);
        }
    }

    nwg::init().expect("Failed to init Native Windows GUI");
    nwg::Font::set_global_family("Microsoft Yahei").expect("Failed to set default font");
    let builder = GuiBuilder::build_ui(Default::default()).expect("Failed to build UI");

    builder.account_edit.set_text(&config.account);
    builder.password_edit.set_text(&config.password);
    match &config.operators as &str {
        "cmcc" => builder.combo_box.set_selection(Some(0)),
        "telecom" => builder.combo_box.set_selection(Some(1)),
        "unicom" => builder.combo_box.set_selection(Some(2)),
        &_ => builder.combo_box.set_selection(Some(0)),
    };
    let state: CheckBoxState = match config.autostart {
        true => CheckBoxState::Checked,
        false => CheckBoxState::Unchecked,
    };
    builder.auto_start.set_check_state(state);

    nwg::dispatch_thread_events();
}
