library vunit_lib;
  context vunit_lib.vunit_context;

library ieee;
  use ieee.std_logic_1164.all;

entity tb_enc_hardcoded is
  generic (
    runner_cfg : string
  );
end entity tb_enc_hardcoded;

architecture behavior of tb_enc_hardcoded is

  -- Input signals
  signal clk       : std_logic := '0';
  signal rst       : std_logic := '0';
  signal plaintext : std_logic_vector(127 downto 0);
  signal key       : std_logic_vector(127 downto 0);

  -- Output signals
  signal done       : std_logic;
  signal ciphertext : std_logic_vector(127 downto 0);

  -- Clock period definition
  constant clk_period : time := 10 ns;

begin

  enc_inst : entity work.aes_enc
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

      if run("hardcoded encryption test") then
        -- Initialize Inputs
        -- p = ab354967 20dff452 7ce28bad 7288e3f4
        -- k = 0388be43 c7f46afd 8d7d55ef b1407298
        -- c = 779a623a c2d10b28 28dd64b5 ecdb7b34
        plaintext <= x"f4e38872ad8be27c52f4df20674935ab";
        key       <= x"987240b1ef557d8dfd6af4c743be8803";
        -- Hold reset state for one cycle
        rst <= '0';
        wait for clk_period * 1;
        rst <= '1';
        wait until done = '1';
        wait for clk_period / 2;
        if (ciphertext = x"347bdbecb564dd28280bd1c23a629a77") then
          report "------------ Passed ------------";
        else
          assert false
            report "------------ Failed ------------";
          report "-------- Output must be: -------";
          report "347bdbecb564dd28280bd1c23a629a77";
        end if;
      end if;

    end loop;

    test_runner_cleanup(runner); -- Simulation ends here

  end process sim_proc;

end architecture behavior;

