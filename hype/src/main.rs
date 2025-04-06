use http_body_util::Empty;
use hyper::Request;
use hyper::body::Bytes;

use hyper_util::client::legacy::{connect::HttpConnector, Client};

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let url = "http://127.0.0.1:10000/1.parquet".parse::<hyper::Uri>()?;
    let client = Client::builder(hyper_util::rt::TokioExecutor::new()).build(HttpConnector::new());

    let req = Request::builder()
        .uri(url)
        .body(Empty::<Bytes>::new())?;

    let resp = client.request(req).await?;

    eprintln!("{:?} {:?}", resp.version(), resp.status());
    eprintln!("{:#?}", resp.headers());

    Ok(())
}
