<script>
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';

	import { module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

	export let data;
	let { item } = data;
	let { variation_options } = item;

	let in_variation;

	let in_values = {};
	for (let i in variation_options) {
		in_values[i] = variation_options[i].join(', ');
	}

	const add_variation = () => {
		if (!in_variation) {
			return;
		}

		in_variation = in_variation.toLowerCase();

		for (let i in variation_options) {
			if (i == in_variation) {
				in_variation = '';
				return;
			}
		}

		variation_options[in_variation] = [];
		in_variation = '';
	};

	const delete_variation = (Variation_name) => {
		let temp = {};
		for (let i in variation_options) {
			if (i != Variation_name) {
				temp[i] = variation_options[i];
			}
		}
		variation_options = temp;
	};

	const update_value = (Variation_name) => {
		let temp1 = in_values[Variation_name].split(',');
		let temp2 = [];
		for (let i in temp1) {
			temp2.push(temp1[i].trim());
		}
		variation_options[Variation_name] = temp2;
	};

	let error;
	const validate = () => {
		error = '';

		if (variation_options.length > 0) {
			for (let i in variation_options) {
				if (variation_options[i].length < 1) {
					error = 'Empty property value';
				}
			}
		}

		!error && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}item_variation/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ variation_options })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.item);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};

	const proc = (v) => v.split(':');
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit Variation</div>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="key">Variation</label>
			<div class="inputGroup horizontal">
				<input
					type="text"
					id="key"
					placeholder="Variation here"
					bind:value={in_variation}
					on:keypress={(e) => {
						if (e.key == 'Enter') {
							add_variation();
						}
					}}
				/>
				<Button
					class="primary"
					name="Submit"
					on:click={() => {
						add_variation();
					}}
				/>
			</div>
		</div>

		{#each Object.entries(variation_options) as [key, values], i (i)}
			<div
				class="inputGroup variation"
				div
				animate:flip={{ delay: 0, duration: 250, easing: backInOut }}
			>
				<div class="h space">
					<label for={key}>
						<span>
							{key}
						</span>
					</label>
					<div class="h">
						<Button
							icon="close"
							icon_size="10"
							class="tiny hover_red"
							on:click={() => {
								delete_variation(key);
							}}
						/>
					</div>
				</div>

				<div class="inputGroup horizontal">
					<input
						type="text"
						id={key}
						placeholder="value here"
						bind:value={in_values[key]}
						on:input={(e) => {
							update_value(key);
						}}
					/>
				</div>

				<div class="value_area">
					{#each values as value, j (j)}
						<div class="h value" animate:flip={{ delay: 0, duration: 250, easing: backInOut }}>
							{#if key == 'size'}
								<button>
									{value}
								</button>
							{:else}
								<button class="default" style:background-color={proc(value)[1]}>
									{proc(value)[0]}
								</button>
							{/if}
						</div>
					{/each}
				</div>
			</div>
		{/each}

		{#if error}
			<p class="error">
				{error}
			</p>
		{/if}
		<div class="inputGroup horizontal">
			<Button
				class="primary"
				name="Submit"
				on:click={() => {
					validate();
				}}
			/>
		</div>
	</form>
</Form>

<style>
	.variation {
		padding: var(--gap1);
		border-radius: var(--brad1);
		border: 2px solid var(--background);
	}

	.value_area {
		display: flex;
		flex-wrap: wrap;

		gap: var(--gap1);
	}
	.value {
		gap: 0;
	}
	span {
		font-weight: 500;
		text-transform: capitalize;
	}

	button {
		--size: 30px;

		all: unset;
		cursor: pointer;
		box-sizing: border-box;

		display: flex;
		justify-content: center;
		align-items: center;

		min-width: var(--size);
		height: var(--size);

		font-size: small;

		padding: 0 var(--gap1);
		border-radius: calc(var(--size) / 2);
		background-color: var(--background);
	}
</style>
