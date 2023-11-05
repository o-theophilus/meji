<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import SVG from '$lib/svg.svelte';

	let item = { ...$module.item };
	let variation = { ...item.variation };
	for (const key in variation) {
		variation[key] = variation[key].join(', ');
	}
	let error = {};
	let input;

	const add_key = () => {
		error = {};
		if (!input) {
			error.variation = 'this field is required';
			return;
		}

		input = input.toLowerCase();

		for (let i in variation) {
			if (i == input) {
				error.variation = 'already available';
				return;
			}
		}

		if (input.startsWith('size')) {
			let match = input.match(/(\d+)-(\d+)/);
			if (match) {
				let start = parseInt(match[1]);
				let end = parseInt(match[2]);

				let n = [];
				for (let i = start; i <= end; i++) {
					n.push(i);
				}
				variation['size'] = n.join(', ');
			}
		} else {
			variation[input] = '';
		}

		input = '';
	};

	const delete_key = (to_remove) => {
		let temp = {};
		for (let i in variation) {
			if (i != to_remove) {
				temp[i] = variation[i];
			}
		}
		variation = temp;
	};

	const clean_value = (key) => {
		let a = variation[key];
		a = a.replace(/\r?\n/g, ',');
		a = a.replace(/\s+/g, ' ');
		a = a.toLowerCase();
		a = a.split(',');
		a = a.map((i) => i.trim());
		a = a.filter(Boolean);
		a = a.filter((v, i, l) => l.indexOf(v) === i);
		a = a.join(', ');
		variation[key] = a;
	};

	const validate = () => {
		error = {};

		for (let key in variation) {
			if (!variation[key]) {
				error[key] = 'empty value';
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		let temp = { ...variation };
		for (let key in temp) {
			temp[key] = temp[key].split(', ');
		}

		$loading = "saving . . .";
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ variation: temp })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'item',
				data: resp.item
			};
			$module = '';
			$toast = {
				status: 200,
				message: 'variation changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Variation</b>
	</svelte:fragment>

	<IG name="variation" {error} let:id>
		<input
			bind:value={input}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					add_key;
				}
			}}
			{id}
			type="text"
			placeholder="variation here"
		/>
		<Button on:click={add_key}>Add</Button>
	</IG>

	{#each Object.keys(variation) as key, i (i)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<IG name={key} {error} let:id>
				<svelte:fragment slot="label">
					<div class="line">
						{key}
						<Button
							class="round small hover_red"
							on:click={() => {
								delete_key(key);
							}}
						>
							<SVG type="close" size="10" />
						</Button>
					</div>
				</svelte:fragment>
				<textarea
					bind:value={variation[key]}
					on:blur={() => {
						clean_value(key);
					}}
					{id}
					placeholder="Options here"
				/>
			</IG>
		</div>
	{/each}

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
	{/if}
	<Button class="primary" on:click={validate}>Save</Button>
</Form>

<style>
	.line {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
	}
</style>
