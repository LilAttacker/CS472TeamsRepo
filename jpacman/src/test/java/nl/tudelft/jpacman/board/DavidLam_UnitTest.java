package nl.tudelft.jpacman.level;

import nl.tudelft.jpacman.sprite.PacManSprites;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class DavidLam_UnitTest {

    private static final PacManSprites SPRITE_STORE = new PacManSprites();
    private final PlayerFactory Factory = new PlayerFactory(SPRITE_STORE);
    private final Player player = Factory.createPacMan();

    @Test
    void testAlive() {
        assertThat(player.isAlive()).isEqualTo(true);
    }

    @Test
    void testSetAlive() {
        player.setAlive(true);
        assertThat(player.isAlive()).isEqualTo(true);

        player.setAlive(false);
        assertThat(player.isAlive()).isEqualTo(false);
    }

    @Test
    void testScore() {
        // Upon initilization, score should be 0
        assertThat(player.getScore()).isEqualTo(0);
    }

    @Test
    void testSetScore() {
        int points = player.getScore();
        player.addPoints(1);

        assertThat(player.getScore()).isEqualTo(points + 1);
    }
}
