<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let item = { ...$module.item };
	let text = `Check Out: ${item.name}`;
</script>

<section>
	<b> Share </b>

	<div class="block">
		<Button
			class="round"
			href="https://www.facebook.com/sharer.php?u={$page.url.href}"
			target="_blank"
			tooltip="Facebook"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="facebook" />
		</Button>

		<Button
			class="round"
			href="http://twitter.com/share?text={text}&url={$page.url.href}&hashtags=meji,shopping"
			target="_blank"
			tooltip="Twitter"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="twitter" />
		</Button>

		<Button
			class="round"
			href="whatsapp://send?text={text}%20{$page.url.href}"
			tooltip="Whatsapp"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="whatsapp" />
		</Button>

		<Button
			class="round"
			href="https://telegram.me/share/url?url={$page.url.href}&text={text}"
			target="_blank"
			tooltip="Telegram"
			on:click={() => {
				$module = '';
			}}
		>
			<SVG type="telegram" />
		</Button>

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
		gap: var(--sp2);
	}
</style>
