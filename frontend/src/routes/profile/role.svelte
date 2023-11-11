<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Card from '$lib/card.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Check from '$lib/button.check.svelte';
	import Role_Ok from './role._ok.svelte';

	export let user;
	let user_roles = [...user.roles];
	let open = true;

	let roles = {
		admin: {
			level_1: [],
			level_2: ['manage_photo'],
			level_3: []
		},
		user: {
			level_1: ['view'],
			level_2: ['view_balance'],
			level_3: ['set_role']
		},
		item: {
			level_1: [],
			level_2: [
				'add',
				'edit_photo',
				'advert',
				'edit_status',
				'edit_name',
				'edit_tag',
				'edit_price',
				'edit_info',
				'edit_variation'
			],
			level_3: []
		},
		voucher: {
			level_1: ['view'],
			level_2: [],
			level_3: ['add', 'view_code']
		},
		log: {
			level_1: ['view'],
			level_2: [],
			level_3: []
		}
	};

	const select_group = (_in = '', _group = '') => {
		let group = [];
		for (const [_cate, _levels] of Object.entries(roles)) {
			for (const [_level, _roles] of Object.entries(_levels)) {
				if (_group == 'level' && _level == _in) {
					for (const _role of _roles) {
						group.push(`${_cate}:${_role}`);
					}
				} else if (_group == 'cate' && _cate == _in) {
					for (const _role of _roles) {
						group.push(`${_cate}:${_role}`);
					}
				} else if (!_group && !_in) {
					for (const _role of _roles) {
						group.push(`${_cate}:${_role}`);
					}
				}
			}
		}

		let add_all = false;
		for (const x of group) {
			if (!user_roles.includes(x)) {
				add_all = true;
				break;
			}
		}

		if (add_all) {
			for (const x of group) {
				if (!user_roles.includes(x)) {
					user_roles.push(x);
				}
			}
			user_roles = user_roles;
		} else {
			user_roles = user_roles.filter((x) => !group.includes(x));
		}
	};

	const select = (role) => {
		if (!user_roles.includes(role)) {
			user_roles.push(role);
			user_roles = user_roles;
		} else {
			user_roles = user_roles.filter((x) => x != role);
		}
	};
</script>

<Card>
	<div class="title">
		Roles
		<ButtonFold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	</div>

	{#if open}
		<br />
		<section transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<span>
				<Button
					class="link small"
					on:click={() => {
						select_group();
					}}
				>
					category
				</Button>
			</span>

			{#each ['level_1', 'level_2', 'level_3'] as level}
				<span>
					<Button
						class="link small"
						on:click={() => {
							select_group(level, 'level');
						}}
					>
						{level.split('_').join(' ')}
					</Button>
				</span>
			{/each}

			{#each Object.entries(roles) as [cate, levels]}
				<span>
					<Button
						class="link small"
						on:click={() => {
							select_group(cate, 'cate');
						}}
					>
						{cate}
					</Button>
				</span>
				{#each Object.entries(levels) as [level, roles]}
					<span>
						{#each roles as role}
							<Check
								active={user_roles.includes(`${cate}:${role}`)}
								on:click={() => {
									select(`${cate}:${role}`);
								}}
							>
								{role.split('_').join(' ')}
							</Check>
						{/each}
					</span>
				{/each}
			{/each}
		</section>

		<br />

		<Button
			class="primary"
			on:click={() => {
				$module = {
					module: Role_Ok,
					key: user.key,
					roles: user_roles
				};
			}}>Ok</Button
		>
	{/if}
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	section {
		display: grid;
		grid-template-columns: repeat(4, auto);
	}

	span {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
		align-items: center;

		outline: 1px solid var(--ac4);
		padding: var(--sp1);
	}
</style>
