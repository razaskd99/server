from typing import List, Optional
from fastapi import HTTPException
from db.connection import get_db_connection
from bid_team.schemas import BidTeamCreate, BidTeam, UpdateBidTeam, GetAllBidTeam


def create_bidteam(item_form_data: BidTeamCreate) -> BidTeam:
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO bid_team (
        tenant_id,
        user_id,
        index,
        title,
        persona,
        created_at
    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """

    values = (
        item_form_data.tenant_id,
        item_form_data.user_id,
        item_form_data.index,       
        item_form_data.title,
        item_form_data.persona,
        item_form_data.created_at
    )

    cursor.execute(query, values)
    new_item = cursor.fetchone()

   
    conn.commit()
    conn.close()

    if new_item:
        return BidTeam(
            bid_team_id=new_item[0],
            tenant_id=new_item[1],
            user_id=new_item[2],
            index=new_item[3],
            title=new_item[4],
            persona=new_item[5],
            created_at=new_item[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Bid Team Detail creation failed")


def get_all_bidteam(tenant_id: int) -> List[GetAllBidTeam]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT bt.*,
            u.first_name,
            u.last_name,
            u.email,
            u.user_profile_photo 
            FROM bid_team bt
            LEFT JOIN users u ON u.user_id = bt.user_id                     
        WHERE bt.tenant_id = %s ;
        """

    cursor.execute(query,(tenant_id, ))
    query_all_items = cursor.fetchall()

    conn.close()
    if query_all_items:
        return [
            GetAllBidTeam(
                bid_team_id=row[0],
                tenant_id=row[1],
                user_id=row[2],
                index=row[3],
                title=row[4],
                persona=row[5],
                created_at=row[6],
                first_name=row[7],
                last_name=row[8],
                email=row[9],
                user_profile_photo=row[10]
            )
            for row in query_all_items
        ]
    else:
        None


def update_bidteam(bid_team_id: int,  item_form_data: UpdateBidTeam) -> Optional[BidTeam]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE bid_team SET 
        user_id = %s,
        index = %s,
        title = %s,
        persona = %s
    WHERE bid_team_id = %s RETURNING *;
    """

    values = (
        item_form_data.user_id,
        item_form_data.index,
        item_form_data.title,
        item_form_data.persona,
        bid_team_id
    )

    cursor.execute(query, values)
    updated_itemm = cursor.fetchone()

    
    conn.commit()
    conn.close()

    if updated_itemm:
        return BidTeam(
                bid_team_id=updated_itemm[0],
                tenant_id=updated_itemm[1],
                user_id=updated_itemm[2],
                index=updated_itemm[3],
                title=updated_itemm[4],
                persona=updated_itemm[5],
                created_at=updated_itemm[6]
            )
    else:
        raise HTTPException(status_code=404, detail="Bid Team update failed")


def delete_bidteam(bid_team_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
   
    query = "DELETE FROM bid_team WHERE bid_team_id = %s RETURNING bid_team_id;"
    cursor.execute(query, (bid_team_id,))
    deleted_item = cursor.fetchone()

    conn.commit()
    conn.close()

    if deleted_item:
        return True
    else:
        return False
    


def get_bidteam_by_id(bid_team_id: int) -> Optional[GetAllBidTeam]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            u.first_name, u.last_name, u.email, u.user_profile_photo 
            FROM bid_team b
            LEFT JOIN users u ON u.user_id = b.user_id                      
        WHERE b.bid_team_id = %s ;
        """

    cursor.execute(query, (bid_team_id,))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return GetAllBidTeam(
                bid_team_id=get_item[0],
                tenant_id=get_item[1],
                user_id=get_item[2],
                index=get_item[3],
                title=get_item[4],
                persona=get_item[5],
                created_at=get_item[6],
                first_name=get_item[7],
                last_name=get_item[8],
                email=get_item[9],
                user_profile_photo=get_item[10]
            )
    else:
        return None


def get_bidteam_by_title(title : str, tenant_id: int) -> Optional[GetAllBidTeam]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.*,
            u.first_name, u.last_name, u.email, u.user_profile_photo 
            FROM bid_team b
            LEFT JOIN users u ON u.user_id = b.user_id                      
        WHERE lower(b.title) = %s AND b.tenant_id = %s;
        """

    cursor.execute(query, (title.lower(), tenant_id))
    get_item = cursor.fetchone()

    conn.close()

    if get_item:
        return GetAllBidTeam(
                bid_team_id=get_item[0],
                tenant_id=get_item[1],
                user_id=get_item[2],
                index=get_item[3],
                title=get_item[4],
                persona=get_item[5],
                created_at=get_item[6],
                first_name=get_item[7],
                last_name=get_item[8],
                email=get_item[9],
                user_profile_photo=get_item[10]
            )
    else:
        return None
    
