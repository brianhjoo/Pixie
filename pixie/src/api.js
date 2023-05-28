import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_PROJECT_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey)


class PixieAPI {
  /** Get all countries */
  static async getCountries() {
    const { data } = await supabase.from("countries").select();
    return data;
  }
}

export default PixieAPI;