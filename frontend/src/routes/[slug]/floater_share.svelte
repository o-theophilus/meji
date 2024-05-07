<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';

	let item = { ...$module.item };
	let text = `Check Out: ${item.name}`;
</script>

<section>
	<b> Share </b>

	<div class="block">
		<BRound
			icon="facebook"
			tooltip="Facebook"
			href="https://www.facebook.com/sharer.php?u={$page.url.href}"
			target="_blank"
			large
			on:click={() => {
				$module = '';
			}}
		/>

		<BRound
			icon="twitter"
			tooltip="Twitter"
			href="http://twitter.com/share?text={text}&url={$page.url.href}&hashtags=meji,shopping"
			target="_blank"
			large
			on:click={() => {
				$module = '';
			}}
		/>

		<BRound
			icon="whatsapp"
			tooltip="Whatsapp"
			href="whatsapp://send?text={text}%20{$page.url.href}"
			large
			on:click={() => {
				$module = '';
			}}
		/>

		<BRound
			icon="telegram"
			tooltip="Telegram"
			href="https://telegram.me/share/url?url={$page.url.href}&text={text}"
			target="_blank"
			large
			on:click={() => {
				$module = '';
			}}
		/>

		<!-- <div class="icon">
		<div class="svg" icon="instagram" ></div>
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
