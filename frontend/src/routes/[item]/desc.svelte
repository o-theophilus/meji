<script>
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_fold.svelte';
	import Button from '$lib/comp/button_fold.svelte';

	import Md from '$lib/comp/marked.svelte';

	export let item = {};
	let open = true && item.desc;
</script>

<Title title="Product Details">
	<Button
		{open}
		on:click={() => {
			open = !open;
		}}
	/>
</Title>
{#if open}
	<Body>
		{#if item.desc}
			<Md md={item.desc} />
		{:else}
			No description
		{/if}
	</Body>
{/if}
