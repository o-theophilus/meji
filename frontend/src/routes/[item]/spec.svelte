<script>
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_fold.svelte';
	import Button from '$lib/comp/button_fold.svelte';

	import Md from '$lib/comp/marked.svelte';

	export let item;
	let open = true && item.spec;
</script>

<Title title="Specifications">
	<Button
		{open}
		on:click={() => {
			open = !open;
		}}
	/></Title
>
{#if open}
	<Body>
		{#if item.spec}
			<Md md={item.spec} />
		{:else}
			No specification
		{/if}
	</Body>
{/if}
