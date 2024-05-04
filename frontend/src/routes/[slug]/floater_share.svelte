<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';

	let item = { ...$module.item };
	let text = `Check Out: ${item.name}`;
</script>

<section>
	<b> Share </b>

	<div class="block">
		<BRound
			size="large"
			href="https://www.facebook.com/sharer.php?u={$page.url.href}"
			target="_blank"
			tooltip="Facebook"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="facebook" />
		</BRound>

		<BRound
			size="large"
			href="http://twitter.com/share?text={text}&url={$page.url.href}&hashtags=meji,shopping"
			target="_blank"
			tooltip="Twitter"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="twitter" />
		</BRound>

		<BRound
			size="large"
			href="whatsapp://send?text={text}%20{$page.url.href}"
			tooltip="Whatsapp"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="whatsapp" />
		</BRound>

		<BRound
			size="large"
			href="https://telegram.me/share/url?url={$page.url.href}&text={text}"
			target="_blank"
			tooltip="Telegram"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="telegram" />
		</BRound>

		<!-- <div class="icon">
		<div class="svg"><SVG type="instagram" /></div>
		</div> -->
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		padding: var(--sp3);
		color: var(--ac1);
		background-color: var(--ac6);
	}
	.block {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--sp1);
	}
</style>
