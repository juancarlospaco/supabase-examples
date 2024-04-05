const https = require('https');

const PROJECT_URL = 'https://utawmowgglsndawzxebx.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_KEY;


class Client {

  constructor(projectUrl, supabaseKey) {
    if (!supabaseKey) {
      console.error("Please set up your SUPABASE_KEY environment variable");
      return;
    }
    this.projectUrl = projectUrl;
    this.supabaseKey = supabaseKey;
    this.basePath = this.projectUrl + "/rest/v1";
    this.pgRange = null;
    this.headers = {
      'apiKey': this.supabaseKey
    };
  }

  connect(path) {
    return new Promise((resolve, reject) => {
      const options = {
        hostname: this.projectUrl.split('//')[1], // Extract hostname from URL
        path: path,
        method: 'GET',
        headers: this.headers
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            const response = JSON.parse(data);
            resolve({ statusCode: res.statusCode, data: response });
          } catch (error) {
            reject(error);
          }
        });
      });

      req.on('error', reject);
      req.end();
    });
  }

  pagination(start, end) {
    this.pgRange = Array.from({ length: end - start + 1 }, (_, i) => start + i); // Generate inclusive range
  }

  paginationRequested() {
    if (this.pgRange) {
      this.headers['Range'] = `${this.pgRange[0]}-${this.pgRange[this.pgRange.length - 1]}`; // Use last element for end
    }
  }

  async resultSet(path, pagination = false) {
    if (pagination) {
      this.paginationRequested();
    }

    try {
      const response = await this.connect(path);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  }

  selectAll(table_name, pagination = false) {
    const path = `${this.basePath}/${table_name}?select=*`;
    this.headers['Authorization'] = `Bearer ${this.supabaseKey}`;
    this.resultSet(path, pagination);
  }

  selectColumns(table_name, pagination = false, cols = []) {
    const csc = cols.join(',');
    const path = `${this.basePath}/${table_name}?select=${csc}`;
    this.headers['Authorization'] = `Bearer ${this.supabaseKey}`;
    this.resultSet(path, pagination);
  }
}


function main() {
  const client = new Client(PROJECT_URL, SUPABASE_KEY);
  client.selectAll("products");
}


main()
