<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';

	let { item } = $module;
	let text = `Check Out: ${item.name}`;
</script>

<section>
	<b> Share </b>

	<div class="block">
		<Button
			icon="facebook"
			href="https://www.facebook.com/sharer.php?u={$page.url.href}"
			target="_blank"
			tooltip="Facebook"
			on:click={() => {
				$module = '';
			}}
		/>
		<Button
			icon="twitter"
			href="http://twitter.com/share?text={text}&url={$page.url.href}&hashtags=meji,shopping"
			target="_blank"
			tooltip="Twitter"
			on:click={() => {
				$module = '';
			}}
		/>

		<Button
			icon="whatsapp"
			href="whatsapp://send?text={text}%20{$page.url.href}"
			tooltip="Whatsapp"
			on:click={() => {
				$module = '';
			}}
		/>

		<Button
			icon="telegram"
			href="https://telegram.me/share/url?url={$page.url.href}&text={text}"
			target="_blank"
			tooltip="Telegram"
			on:click={() => {
				$module = '';
			}}
		/>

		<!-- <div class="icon">
		<div class="svg"><SVG type="instagram" /></div>
		</div> -->
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);

		padding: var(--gap3);
		color: var(--font1);
		background-color: var(--foreground);
	}
	.block {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--gap2);
	}
</style>
