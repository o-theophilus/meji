<script>
	import { module } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import Form from './__receiver_form.svelte';

	export let order;
	export let previous_recipients;
	$: r = order.recipient;
	$: a = r.address;

	$: complete_address =
		r.name && r.phone && a.line && a.state && a.country && a.local_area && a.postal_code;
</script>

<div class="bold">
	Receiver's Information

	{#if order.status == 'pending'}
		<Button
			class="link"
			name="Edit"
			on:click={() => {
				$module = {
					module: Form,
					order,
					previous_recipients
				};
			}}
		/>
	{/if}
</div>

<p>
	Name:
	{#if r.name}
		{r.name}
	{:else}
		No Name
	{/if}
	<br />
	Phone:
	{#if r.phone}
		{r.phone}
	{:else}
		No Phone
	{/if}
	<br />
	Address:
	{#if complete_address}
		{a.line}, {a.local_area}, {a.state}, {a.country}, {a.postal_code}.
	{:else}
		No Address
	{/if}
</p>

<style>
	p {
		color: var(--ac2);
	}
	.bold {
		font-weight: 500;
	}
</style>
