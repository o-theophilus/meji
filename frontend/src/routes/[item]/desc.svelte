<script>
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_fold.svelte';
	import Button from '$lib/comp/button_fold.svelte';

	import Md from '$lib/comp/marked.svelte';

	export let item = {};
	let open_desc = true && item.desc;
	let open_spec = true && item.spec;
</script>

<Title title="Product Details">
	<Button
		open={open_desc}
		on:click={() => {
			open_desc = !open_desc;
		}}
	/>
</Title>
{#if open_desc}
	<Body>
		{#if item.desc}
			<Md md={item.desc} />
		{:else}
			No description
		{/if}
	</Body>
{/if}

<Title title="Specifications">
	<Button
		open={open_spec}
		on:click={() => {
			open_spec = !open_spec;
		}}
	/></Title
>
{#if open_spec}
	<Body>
		{#if item.spec}
			<Md md={item.spec} />
		{:else}
			No specification
		{/if}
	</Body>
{/if}
