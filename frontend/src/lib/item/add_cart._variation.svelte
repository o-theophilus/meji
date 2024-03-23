<script>
	import { module, user, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import Quantity from './quantity.svelte';
	import Value from '$lib/item/variation_value.svelte';
	import SVG from '$lib/svg.svelte';

	let item = { ...$module.item };
	let { variation } = item;

	let error = {};
	let vars_ = {};
	let quantity = 1;

	const validate = () => {
		error = {};

		for (let i of Object.keys(variation)) {
			if (!vars_[i]) {
				error[i] = `Please select a ${i}`;
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		let key = `${item.key}_${JSON.stringify(vars_)}`;
		if (!$user.cart.includes(key)) {
			$user.cart.push(key);
			$user = $user;
		}
		$module = '';
		$toast = {
			status: 200,
			message: `${item.name} added to cart`
		};

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				variation: vars_,
				quantity,
				ops: 'add'
			})
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$user.cart = resp.user.cart;
		} else {
			$toast = {
				status: 400,
				message: resp.error
			};
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Select variation</b>
	</svelte:fragment>

	{#each Object.entries(variation) as [key, values]}
		<div class="property">
			<span class="bold">{key}</span>

			<div class="value_row">
				{#each values as value, i}
					<!-- {#if i != 0}, &nbsp; {/if} -->
					<Value
						button
						active={vars_[key] == value}
						{value}
						on:click={() => {
							vars_[key] = value;
						}}
					/>
				{/each}
			</div>

			{#if error[key]}
				<p class="error">
					{error[key]}
				</p>
			{/if}
		</div>
		<br />
	{/each}

	<div class="property">
		<span class="bold"> quantity </span>
		<Quantity
			quantity={1}
			on:done={(e) => {
				quantity = e.detail.quantity || 1;
			}}
		/>

		{#if error.quantity}
			<p class="error">
				{error.quantity}
			</p>
		{/if}
	</div>

	<br />

	<Button
		class="primary"
		on:click={() => {
			validate();
		}}
	>
		<SVG type="cart_add" size="18" />
		Add to cart
	</Button>
</Form>

<style>
	.property {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
		
		color: var(--ac1);
	}

	.bold {
		font-weight: 500;
		text-transform: capitalize;
	}
	
	.value_row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
	}
</style>
