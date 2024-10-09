library vunit_lib;
  context vunit_lib.vunit_context;

library ieee;
  use ieee.std_logic_1164.all;

entity tb_enc_generics is
  generic (
    runner_cfg          : string;
    key                 : std_logic_vector(127 downto 0);
    plaintext           : std_logic_vector(127 downto 0);
    expected_ciphertext : std_logic_vector(127 downto 0)
  );
end entity tb_enc_generics;

architecture behavior of tb_enc_generics is

  -- Input signals
  signal clk : std_logic := '0';
  signal rst : std_logic := '0';

  -- Output signals
  signal done       : std_logic;
  signal ciphertext : std_logic_vector(127 downto 0);

  -- Clock period definition
  constant clk_period : time := 10 ns;

begin

  enc_inst : entity  work.aes_enc
    port map (
      clk        => clk,
      rst        => rst,
      key        => key,
      plaintext  => plaintext,
      ciphertext => ciphertext,
      done       => done
    );

  -- clock process
  clk <= not clk after clk_period / 2;

  -- Simulation process
  sim_proc : process is
  begin

    test_runner_setup(runner, runner_cfg);

    while test_suite loop

      if run("generic encryption test") then
        -- Hold reset state for one cycle
        rst <= '0';
        wait for clk_period * 1;
        rst <= '1';

        wait until done = '1';
        wait for clk_period / 2;
        check(ciphertext = expected_ciphertext, "Got 0x" & to_hstring(ciphertext) & ". Expected 0x" & to_hstring(expected_ciphertext));
      elsif run("random generic encryption test") then
        -- Hold reset state for one cycle
        rst <= '0';
        wait for clk_period * 1;
        rst <= '1';

        wait until done = '1';
        wait for clk_period / 2;
        check(ciphertext = expected_ciphertext, "Got 0x" & to_hstring(ciphertext) & ". Expected 0x" & to_hstring(expected_ciphertext));
      end if;

    end loop;

    test_runner_cleanup(runner); -- Simulation ends here

  end process sim_proc;

end architecture behavior;

