<script>
	import { Datetime } from '$lib/macro';
	let { data, columns } = $props();

	let _cols = [];
	for (const x of columns) {
		let temp = x.split(':');
		let dict = { name: temp[0] };
		if (temp[1]) dict.type = temp[1];
		_cols.push(dict);
	}
</script>

<div class="table-wrapper">
	<table>
		<thead>
			<tr>
				{#each _cols as x}
					<th>{x.name}</th>
				{/each}
			</tr>
		</thead>

		<tbody>
			{#each data as row}
				<tr>
					{#each _cols as col}
						<td>
							{#if col.type?.startsWith('href')}
								<a href={row[col.type]}>
									{row[col.name]}
								</a>
							<!-- {:else if col.type == 'date'}
								<Datetime datetime={row[col.name]} type="date_numeric"></Datetime>
								<br />
								<Datetime datetime={row[col.name]} type="time_12h"></Datetime> -->
							{:else}
								{row[col.name]}
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.table-wrapper {
		width: 100%;
		overflow-x: auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.7rem;
	}

	thead {
		background-color: var(--bg2);

		th {
			text-align: left;
			padding: 4px 8px;
			font-weight: 800;
			text-transform: capitalize;
		}
	}

	tbody {
		tr:hover {
			background-color: var(--bg2);
		}
		td {
			padding: 2px 8px;
		}
	}

	tr {
		border-bottom: 1px solid var(--ol);
		&:last-child {
			border-bottom: none;
		}
	}

	a {
		text-decoration: none;
		color: var(--cl1);
	}
</style>
