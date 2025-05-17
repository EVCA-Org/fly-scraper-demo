-- Create table for scraped data
CREATE TABLE IF NOT EXISTS scraped_data (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT,
  source TEXT,
  scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster querying
CREATE INDEX IF NOT EXISTS idx_scraped_data_scraped_at ON scraped_data(scraped_at);

-- Add RLS (Row Level Security) policies
ALTER TABLE scraped_data ENABLE ROW LEVEL SECURITY;

-- Create policy allowing authenticated users to read all data
CREATE POLICY read_policy ON scraped_data 
  FOR SELECT 
  TO authenticated 
  USING (true);

-- Create policy allowing service role to insert data
CREATE POLICY insert_policy ON scraped_data 
  FOR INSERT 
  TO authenticated 
  WITH CHECK (true);
