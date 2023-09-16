<script>
	import { module } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import Form from './_receiver_form.svelte';

	export let order;
	export let previous_recipients;
	$: r = order.recipient;
	$: a = r.address;
</script>

<div class="bold">
	Receiver's Information

	{#if order.status == 'pending'}
		<Button
			class="link"
			on:click={() => {
				$module = {
					module: Form,
					order,
					previous_recipients
				};
			}}
		>
			Edit
		</Button>
	{/if}
</div>

<div class="grid">
	<div>Name:</div>
	<div>
		{#if r.name}
			{r.name}
		{:else}
			No Name
		{/if}
	</div>

	<div>Phone:</div>
	<div>
		{#if r.phone}
			{r.phone}
		{:else}
			No Phone
		{/if}
	</div>

	<div>Address:</div>
	<div>
		{#if a.line && a.state && a.country && a.local_area && a.postal_code}
			{a.line}, {a.local_area}, {a.state}, {a.country}, {a.postal_code}.
		{:else}
			No Address
		{/if}
	</div>
</div>

<style>
	.bold {
		font-weight: 500;
	}
	.grid {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content auto;
		color: var(--ac2);
	}
</style>
